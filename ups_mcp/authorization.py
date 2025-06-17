import requests
import time

class OAuthManager:
    def __init__(self, token_url, client_id, client_secret):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expiry = 0

    def get_access_token(self):
        # If token is still valid, return it
        if self.access_token and time.time() < self.token_expiry - 60:
            return self.access_token

        # Validate client credentials
        if not self.client_id or not self.client_secret:
            raise ValueError("CLIENT_ID and CLIENT_SECRET must be set in environment variables.")

        data = {
            "grant_type": "client_credentials"
        }

        response = requests.post(
            self.token_url,
            data=data,
            auth=(self.client_id, self.client_secret)
        )
        response.raise_for_status()
        token_data = response.json()
        self.access_token = token_data["access_token"]
        self.token_expiry = time.time() + int(token_data.get("expires_in", 0))
        return self.access_token