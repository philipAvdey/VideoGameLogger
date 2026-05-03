# TODO: create endpoints
# TODO: probably should use multiple files for different purposes; e.g. login, user_services, data_services, etc.

import os
import uuid
import time
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from services.igdb.igdb_service import IgdbAPIService


load_dotenv()
app = Flask(__name__)
CORS(app)
IGDB_CLIENT_SECRET = os.getenv("IGDB_CLIENT_SECRET")
IGDB_CLIENT_ID = os.getenv("IGDB_CLIENT_ID")

game_service = IgdbAPIService(IGDB_CLIENT_SECRET, IGDB_CLIENT_ID)

#temporary local storage --> change to DynamoDB
rated_games = []
#tracks requests for each user
rate_limit = {}
#max requests limit/time window
RATE_LIMIT = 100
TIME_WINDOW = 60

def is_rate_limited(username):
    now = time.time()

    #adds user to rate limit's list if first time
    if username not in rate_limit:
        rate_limit[username] = {
            "count": 0,
            "window_start":now
        }
    #user's rate limit to track
    user_limit = rate_limit[username]

    #resets window if time expires
    if now - user_limit["window_start"] >= TIME_WINDOW:
        user_limit["window_start"] = now
        user_limit["count"] = 1
        return False

    #increment user's rate limit by 1
    user_limit["count"] += 1

    #returns true if limit is reached
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
        games = []
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
                {
                    "id": str(game.get("id")),
                    "title": game.get("name", "Unknown"),
                    "releaseDate": release_date,
                    "coverArt": (
                        f"https:{game.get('cover', {}).get('url', '')}".replace("t_thumb", "t_cover_big")
                        if game.get("cover")
                        else "https://via.placeholder.com/300x400?text=No+Cover"
                    ),
                    "ratingCount": int(game.get("rating_count", 0)),
                }
            )
        return jsonify({"games": games})
    except Exception as e:
        print(f"Search error: {str(e)}")
        import traceback

        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# POST Endpoint: adds new game rating
@app.route("/api/ratings", methods=["POST"])
def add_ratings():
    data = request.get_json()

    #checks if JSON
    if not data:
        return jsonify({"error": "No data"}), 400

    #gets username from json
    username = data.get("username")

    #if no username, through error
    if not username:
        return jsonify({"error": "No username"}), 400

    #rate limiting for user
    if is_rate_limited(username):
        return jsonify({"error": "Too many requests"}), 429

    #makes sure title and rating exist before adding the rating
    if "title" not in data or "rating" not in data:
        return jsonify({"error": "Must have a title and rating"}), 400

    #creates a new rating to store
    new_rating = {
        "ratingId": str(uuid.uuid4()), #unique id for each game being stored
        "username": username,
        "title": data.get("title"),         #game title
        "rating": data.get("rating"),
        "dateCompleted": data.get("dateCompleted", ""),
        "releaseDate": data.get("releaseDate", "")
    }

    #saves new rating to temp local list
    rated_games.append(new_rating)

    return jsonify({
        "message": "Game rating added",
        "coverArt": data.get("coverArt", ""),
        "releaseDate": data.get("releaseDate", ""),
        "rating": new_rating
    }), 201


# GET Endpoint: gets all rated games
@app.route("/api/ratings", methods=["GET"])
def get_ratings():
    #username comes from URL query; ex: /api/ratings?username=hank
    #later with login -> username = current_user
    username = request.args.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    #rate limit per user
    if is_rate_limited(username):
        return jsonify({"error": "Too many requests"}), 429

    #returns user's ratings
    user_ratings = []

    #loop to go through every saved game in list
    for game in rated_games:
        if game["username"] == username:    #matches rating to user
            user_ratings.append(game)       #adds rating to user's list

    return jsonify({"userRatings": user_ratings})


# PUT Endpoint: updates a game rating
@app.route("/api/ratings/<rating_id>", methods=["PUT"])
def update_rating(rating_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data"}), 400

    #gets username from json
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    #rate limit
    if is_rate_limited(username):
        return jsonify({"error": "Too many requests"}), 429

    #go through all rating searching for match(user_ratingID & username)
    for game in rated_games:
        #checks for a match with ratingID and username
        if game["ratingId"] == rating_id and game["username"] == username:
            #updates game rating
            game["rating"] = data.get("rating", game["rating"])

            return jsonify({
                "message": "Game rating updated",
                "rating": game
            }), 200

    return jsonify({
        "error": "Rating not found"
    }), 404


# DELETE Endpoint: deletes a game rating
@app.route("/api/ratings/<rating_id>", methods=["DELETE"])
def delete_rating(rating_id):
    username = request.args.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    #rate limit
    if is_rate_limited(username):
        return jsonify({"error": "Too many requests"}), 429

    #looks through list of rating to find the correct one
    for game in rated_games:
        #ratingId and username must match
        if game["ratingId"] == rating_id and game["username"] == username:
            #deletes rating
            rated_games.remove(game)
            return jsonify({
                "message": "Game rating deleted",
            })
    return jsonify({
        "error": "Rating not found"
    }), 404