import requests
from requests.auth import HTTPBasicAuth
import os
import uuid
import json
from . import constants

BASE_URL = constants.CIE_URL

def track_package(inquiryNum: str, locale: str, returnSignature: str, returnMilestones: str, returnPOD: str):
    url = f"{BASE_URL}/api/track/v1/details/{inquiryNum}"

    query = {
        "locale": locale,
        "returnSignature": returnSignature,
        "returnMilestones": returnMilestones,
        "returnPOD": returnPOD
    }

    token = create_token()

    headers = {
        "transId": str(uuid.uuid4()),
        "transactionSrc": "Local MCP Server",
        "Authorization": f"Bearer {token['access_token']}"
    }

    response = requests.get(url, headers=headers, params=query)

    response = response.text

    return str(response)

def create_token():
    url = f"{BASE_URL}/security/v1/oauth/token"

    clientId = os.getenv("CLIENT_ID")
    clientSecret = os.getenv("CLIENT_SECRET")

    if not clientId or not clientSecret:
        raise ValueError("CLIENT_ID and CLIENT_SECRET must be set in environment variables.")

    auth = HTTPBasicAuth(clientId, clientSecret)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "client_credentials",
    }

    response = requests.post(url, headers=headers, data=data, auth=auth)

    if response.status_code != 200:
        raise ValueError(f"Error creating token: {response.text}")

    return response.json()