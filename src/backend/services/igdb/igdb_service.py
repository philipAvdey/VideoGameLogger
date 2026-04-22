import time
import requests


class IgdbAPIService:

    def __init__(self, secret, id):
        self.secret = secret
        self.id = id
        self.base_url = "https://id.twitch.tv/oauth2"
        self.igdb_api_url = "https://api.igdb.com/v4"
        self.token = None
        self.expires_at = 0

    def _get_token(self):
        # return cached token if possible
        if self.token and time.time() < self.expires_at - 300:
            return self.token

        # TODO: rate limiting?

        response = requests.post(
            f"{self.base_url}/token",
            params={
                "client_id": self.id,
                "client_secret": self.secret,
                "grant_type": "client_credentials",
            },
        )
        response.raise_for_status()

        json_response = response.json()
        self.token = json_response["access_token"]
        self.expires_at = time.time() + json_response["expires_in"]

        return self.token

    def search_games(self, query: str):
        """Search for games by name using IGDB API"""
        token = self._get_token()
        headers = {
            "Client-ID": self.id,
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        # IGDB API endpoint for games
        body = f'search "{query}"; fields id,name,cover.url,first_release_date,rating_count; limit 10;'

        response = requests.post(
            f"{self.igdb_api_url}/games", headers=headers, data=body
        )
        response.raise_for_status()

        return response.json()
