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

load_dotenv()
app = Flask(__name__)
CORS(app)

# DynamoDB setup
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1'),
    endpoint_url=os.getenv('AWS_ENDPOINT_URL'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'test'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'test')
)

table: Table = dynamodb.Table('Users')


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

# TODO: implement with dybamodb (not sure how)
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


@app.route("/api/igdb/auth/token", methods=["POST"])
def get_igdb_token():
    if IGDB_CLIENT_SECRET is None or IGDB_CLIENT_ID is None:
        return jsonify({"error": "Credentials not set"}), 500
    token = game_service._get_token()
    return jsonify({"access_token": token})


@app.route("/api/igdb/search", methods=["GET"])
def search_games():
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
    response = table.get_item(Key={'userId': user_id})
    if 'Item' not in response:
        return jsonify({"error": "User not found"}), 404
    
    # creates a new rating to store
    new_game = Game.from_dict(data)
    
    user = User.from_dict(response['Item'])
    user.diary.append(new_game.to_dict())

    table.put_item(Item=user.to_dict())
    return jsonify(new_game.to_dict()), 201


# GET Endpoint: gets all rated games
@app.route("/api/ratings", methods=["GET"])
def get_ratings():
    # user_id comes from URL query; ex: /api/ratings?user_id=abc123
    # later with login -> user_id = current_user.id
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # rate limit per user
    if is_rate_limited(user_id):
        return jsonify({"error": "Too many requests"}), 429

    # returns user's ratings
    user_ratings = []

    # loop to go through every saved game in list
    for game in rated_games:
        if game.userId == user_id:  # matches rating to user
            user_ratings.append(game)  # adds rating to user's list
    return jsonify({"userRatings": [rating.__dict__ for rating in user_ratings]})


# PUT Endpoint: updates a game rating
@app.route("/api/ratings/<rating_id>", methods=["PUT"])
def update_rating(rating_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data"}), 400

    # gets user ID from json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # rate limit
    if is_rate_limited(user_id):
        return jsonify({"error": "Too many requests"}), 429

    # go through all rating searching for match(user_ratingID & user_id)
    for game in rated_games:
        # checks for a match with ratingID and user_id
        if game.ratingId == rating_id and game.userId == user_id:
            # updates game rating and date
            game.rating = data.get("rating", game.rating)
            game.dateCompleted = data.get("dateCompleted", game.dateCompleted)

            return (
                jsonify({"message": "Game rating updated", "rating": game.__dict__}),
                200,
            )

    return jsonify({"error": "Rating not found"}), 404


# DELETE Endpoint: deletes a game rating
@app.route("/api/ratings/<rating_id>", methods=["DELETE"])
def delete_rating(rating_id):
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # rate limit
    if is_rate_limited(user_id):
        return jsonify({"error": "Too many requests"}), 429

    # looks through list of rating to find the correct one
    for game in rated_games:
        # ratingId and user_id must match
        if game.ratingId == rating_id and game.userId == user_id:
            # deletes rating
            rated_games.remove(game)
            return jsonify(
                {
                    "message": "Game rating deleted",
                }
            )
    return jsonify({"error": "Rating not found"}), 404
