# TODO: create endpoints
# TODO: probably should use multiple files for different purposes; e.g. login, user_services, data_services, etc.

import os
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
