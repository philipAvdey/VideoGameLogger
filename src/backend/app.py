# TODO: create endpoints
# TODO: probably should use multiple files for different purposes; e.g. login, user_services, data_services, etc.


import os
import uuid
import time
from datetime import datetime
from typing import List

from dotenv import load_dotenv
from flask import Flask, json, jsonify, request
from flask_cors import CORS

from services.igdb.igdb_service import IgdbAPIService

from models.search_result import SearchResult
from models.video_game import Game
from models.user import User

from mypy_boto3_dynamodb.service_resource import Table
import boto3

from services.auth_service import create_auth_blueprint

load_dotenv()
app = Flask(__name__)
CORS(app)

# DynamoDB setup
aws_resource_kwargs = {}
endpoint_url = os.getenv("AWS_ENDPOINT_URL")
if endpoint_url:
    aws_resource_kwargs["endpoint_url"] = endpoint_url
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
if aws_access_key_id and aws_secret_access_key:
    aws_resource_kwargs["aws_access_key_id"] = aws_access_key_id
    aws_resource_kwargs["aws_secret_access_key"] = aws_secret_access_key
aws_session_token = os.getenv("AWS_SESSION_TOKEN")
if aws_session_token:
    aws_resource_kwargs["aws_session_token"] = aws_session_token

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-2"),
    **aws_resource_kwargs,
)

table: Table = dynamodb.Table("VideoGameLogger")


IGDB_CLIENT_SECRET = os.getenv("IGDB_CLIENT_SECRET")
IGDB_CLIENT_ID = os.getenv("IGDB_CLIENT_ID")

game_service = IgdbAPIService(IGDB_CLIENT_SECRET, IGDB_CLIENT_ID)

# temporary local storage --> change to DynamoDB
rated_games: List[Game] = []
# tracks requests for each user
rate_limit = {}
# max requests limit/time window
RATE_LIMIT = 100
TIME_WINDOW = 60


def is_rate_limited(user_id):
    now = time.time()

    # adds user to rate limit's list if first time
    if user_id not in rate_limit:
        rate_limit[user_id] = {"count": 0, "window_start": now}
    # user's rate limit to track
    user_limit = rate_limit[user_id]

    # resets window if time expires
    if now - user_limit["window_start"] >= TIME_WINDOW:
        user_limit["window_start"] = now
        user_limit["count"] = 1
        return False

    # increment user's rate limit by 1
    user_limit["count"] += 1

    # returns true if limit is reached
    if user_limit["count"] > RATE_LIMIT:
        return True
    return False


# registers the auth blueprint so Flask can use the login and create account routes
app.register_blueprint(create_auth_blueprint(table, is_rate_limited))


@app.route("/api/igdb/auth/token", methods=["POST"])
def get_igdb_token():
    """Get IGDB API access token.

    Request Body:
        {} (empty)

    Returns:
        200 - IGDB access token:
            {
                "access_token": str - IGDB API token
            }
        500 - Credentials not configured:
            {
                "error": str - Error message
            }
    """
    if IGDB_CLIENT_SECRET is None or IGDB_CLIENT_ID is None:
        return jsonify({"error": "Credentials not set"}), 500
    token = game_service._get_token()
    return jsonify({"access_token": token})


@app.route("/api/igdb/search", methods=["GET"])
def search_games():
    """Search for games.

    Request Body:
        {
            "query": str (required) - Video game name to search for
        }

    Returns:
        200 - List of games matching query:
            [
                {
                    "id": int - Game ID
                    "title": str - Game title
                    "releaseDate": str - Game release date
                    "coverArt": str - link to game cover art
                    "ratingCount": int - num of ratings this game has
                }
            ]
        500 - Internal error:
            {
                "Search error": str - Error message
            }
    """
    query = request.args.get("query", "")

    if not query or len(query.strip()) == 0:
        return jsonify({"error": "Query parameter is required"}), 400

    try:
        results = game_service.search_games(query)
        games: List[SearchResult] = []
        for game in results:
            # Convert Unix timestamp to ISO date string
            release_timestamp = game.get("first_release_date")
            release_date = ""
            if release_timestamp:
                try:
                    release_date = datetime.fromtimestamp(release_timestamp).strftime(
                        "%Y-%m-%d"
                    )
                except (ValueError, OSError):
                    release_date = ""

            games.append(
                SearchResult(
                    id=str(game.get("id")),
                    title=game.get("name", "Unknown"),
                    releaseDate=release_date,
                    coverArt=(
                        f"https:{game.get('cover', {}).get('url', '')}".replace(
                            "t_thumb", "t_cover_big"
                        )
                        if game.get("cover")
                        else "https://via.placeholder.com/300x400?text=No+Cover"
                    ),
                    ratingCount=int(game.get("rating_count", 0)),
                )
            )
        return jsonify({"games": [game.__dict__ for game in games]})
    except Exception as e:
        print(f"Search error: {str(e)}")
        import traceback

        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# POST Endpoint: adds new game rating to corresponding user ID
@app.route("/api/ratings", methods=["POST"])
def add_ratings():
    """Add a new game rating for a user.

    Request Body:
        {
            "user_id": str (required) - User ID
            "title": str (required) - Game title
            "rating": int (required) - Rating value (1-5)
            "gameId": str - Game ID
            "dateCompleted": str - Date Game completed
            "releaseDate": str - Game release date
            "coverArt": str - link to game cover art
            "ratingId": str - ID of this diary entry (game rating)
        }

    Returns:
        201 - Game rating created:
            {
                "user_id": str (required) - User ID
                "title": str (required) - Game title
                "rating": int (required) - Rating value (1-5)
                "gameId": str - Game ID
                "dateCompleted": str - Date Game completed
                "releaseDate": str - Game release date
                "coverArt": str - link to game cover art
                "ratingId": str - ID of this diary entry (game rating)
            }
        400 - Bad request (missing data/fields)
        404 - User not found
        429 - Too many requests (rate limited)

    """

    data = request.get_json()

    # checks if JSON
    if not data:
        return jsonify({"error": "No data"}), 400

    # gets user ID from json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # rate limiting for user
    if is_rate_limited(user_id):
        return jsonify({"error": "Too many requests"}), 429

    # makes sure title and rating exist before adding the rating
    if "title" not in data or "rating" not in data:
        return jsonify({"error": "Must have a title and rating"}), 400

    # check if user exists in DB
    response = table.get_item(Key={"user_id": user_id})
    if "Item" not in response:
        return jsonify({"error": "User not found"}), 404

    # creates a new rating to store
    new_game = Game.from_dict(data)

    user = User.from_dict(response["Item"])
    user.diary.append(new_game.to_dict())

    table.put_item(Item=user.to_dict())
    return jsonify(new_game.to_dict()), 201


# GET Endpoint: gets all rated games
@app.route("/api/ratings", methods=["GET"])
def get_ratings():
    """Get all game ratings for a user.

    Query Parameters:
        user_id: str (required) - User ID (inside URL, e.g., /api/ratings?user_id=abc123)

    Returns:
        200 - List of user ratings:
            {
                "userRatings": [
                    {
                        "user_id": str (required) - User ID
                        "title": str (required) - Game title
                        "rating": int (required) - Rating value (1-5)
                        "gameId": str - Game ID
                        "dateCompleted": str - Date Game completed
                        "releaseDate": str - Game release date
                        "coverArt": str - link to game cover art
                        "ratingId": str - ID of this diary entry (game rating)
                    }
                ]
            }
        400 - Missing user_id parameter
        404 - User not found
        429 - Too many requests (rate limited)

    TODO: [ADD MORE DETAILS HERE]
    """
    # user_id comes from URL query; ex: /api/ratings?user_id=abc123
    # later with login -> user_id = current_user.id
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # rate limit per user
    if is_rate_limited(user_id):
        return jsonify({"error": "Too many requests"}), 429

    response = table.get_item(Key={"user_id": user_id})
    if "Item" not in response:
        return jsonify({"error": "User not found"}), 404

    user = User.from_dict(response["Item"])
    print(user.diary)
    return jsonify({"userRatings": user.diary})


# PUT Endpoint: updates a game rating
@app.route("/api/ratings/<rating_id>", methods=["PUT"])
def update_rating(rating_id):
    """Update an existing game rating.

    Path Parameters:
        rating_id: str (required) - Rating ID to update

    Request Body:
        {
            "user_id": str (required) - User ID
            "title": str (required) - Game title
            "rating": int (required) - Rating value (1-5)
            "gameId": str - Game ID
            "dateCompleted": str - Date Game completed
            "releaseDate": str - Game release date
            "coverArt": str - link to game cover art
            "ratingId": str - ID of this diary entry (game rating)
        }

    Returns:
        200 - Updated game rating:
            {
                "user_id": str (required) - User ID
                "title": str (required) - Game title
                "rating": int (required) - Rating value (1-5)
                "gameId": str - Game ID
                "dateCompleted": str - Date Game completed
                "releaseDate": str - Game release date
                "coverArt": str - link to game cover art
                "ratingId": str - ID of this diary entry (game rating)
            }
        400 - Bad request (missing data)
        404 - User or game rating not found
        429 - Too many requests (rate limited)

    """
    data = request.get_json()
    # checks if JSON
    if not data:
        return jsonify({"error": "No data"}), 400

    # gets user ID from json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # rate limiting for user
    if is_rate_limited(user_id):
        return jsonify({"error": "Too many requests"}), 429

    # check if user exists in DB
    response = table.get_item(Key={"user_id": user_id})
    if "Item" not in response:
        return jsonify({"error": "User not found"}), 404

    user = User.from_dict(response["Item"])
    game_to_update_index = next(
        (i for i, g in enumerate(user.diary) if g["ratingId"] == rating_id), None
    )
    if game_to_update_index is None:
        return jsonify({"error": "Game not found"}), 404

    updated_game = Game.from_dict(
        {
            **user.diary[game_to_update_index],
            **data,
        }
    )
    user.diary[game_to_update_index] = updated_game.to_dict()

    table.put_item(Item=user.to_dict())
    return jsonify(updated_game.to_dict())


# DELETE Endpoint: deletes a game rating
@app.route("/api/ratings/<rating_id>", methods=["DELETE"])
def delete_rating(rating_id):
    """Delete a game rating for a user.

    Path Parameters:
        rating_id: str (required) - Rating ID to delete

    Query Parameters:
        user_id: str (required) - User ID (e.g., /api/ratings/<id>?user_id=abc123)

    Returns:
        200 - Rating deleted successfully:
            {
                "success": bool - True if deleted
            }
        400 - Missing user_id parameter
        404 - User or game rating not found
        429 - Too many requests (rate limited)

    """
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # rate limit
    if is_rate_limited(user_id):
        return jsonify({"error": "Too many requests"}), 429

    response = table.get_item(Key={"user_id": user_id})
    if "Item" not in response:
        return jsonify({"error": "User not found"}), 404

    user = User.from_dict(response["Item"])
    game_to_delete_index = next(
        (i for i, g in enumerate(user.diary) if g["ratingId"] == rating_id), None
    )
    if game_to_delete_index is None:
        return jsonify({"error": "Game not found"}), 404

    user.diary.pop(game_to_delete_index)

    table.put_item(Item=user.to_dict())
    return jsonify({"success": True})
