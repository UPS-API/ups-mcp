import requests
from requests.auth import HTTPBasicAuth
import os
import uuid
import json
from . import constants
from .authorization import OAuthManager
from dotenv import load_dotenv

class ToolManager:
    def __init__(self):
        load_dotenv()
        if os.getenv("ENVIRONMENT") == "production":
            self.base_url = constants.PRODUCTION_URL
        else:
            self.base_url = constants.CIE_URL

        self.token_manager = OAuthManager(
            token_url=f"{self.base_url}/security/v1/oauth/token",
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET")
        )

    def track_package(self, inquiryNum: str, locale: str, returnSignature: bool, returnMilestones: bool, returnPOD: bool):
        url = f"{self.base_url}/api/track/v1/details/{inquiryNum}"

        query = {
            "locale": locale,
            "returnSignature": returnSignature,
            "returnMilestones": returnMilestones,
            "returnPOD": returnPOD
        }

        token = self.token_manager.get_access_token()

        headers = {
            "transId": str(uuid.uuid4()),
            "transactionSrc": "Local MCP Server",
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(url, headers=headers, params=query)

        if response.status_code != 200:
            raise ValueError(f"Error tracking package: {response.text}")

        response = response.text

        return str(response)