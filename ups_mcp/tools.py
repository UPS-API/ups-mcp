import requests
from requests.auth import HTTPBasicAuth
import os
import uuid
import json
from . import constants
from .authorization import OAuthManager
from dotenv import load_dotenv

class ToolManager:
    def __init__(self, base_url, client_id, client_secret):
        self.base_url = base_url

        self.token_manager = OAuthManager(
            token_url=f"{self.base_url}/security/v1/oauth/token",
            client_id=client_id,
            client_secret=client_secret
        )

    def validate_address(self, addressLine1: str, addressLine2: str, politicalDivision1: str, politicalDivision2: str, zipPrimary: str, zipExtended: str, urbanization: str, countryCode: str):
        url = f"{self.base_url}/api/addressvalidation/v1/1"

        query = {
            "regionalrequestindicator": False,
            "maximumcandidatelistsize": 3
        }

        token = self.token_manager.get_access_token()

        headers = {
            "transId": str(uuid.uuid4()),
            "transactionSrc": "Local MCP Server",
            "Authorization": f"Bearer {token}"
        }

        addressLineList = [addressLine1]

        if addressLine2:
            addressLineList.append(addressLine2)

        addressKeyFormat = {
            "AddressLine": addressLineList,
            "PoliticalDivision2": politicalDivision2,
            "PoliticalDivision1": politicalDivision1,
            "PostcodePrimaryLow": zipPrimary,
            "CountryCode": countryCode
        }

        if urbanization:
            addressKeyFormat["Urbanization"] = urbanization

        if zipExtended:
            addressKeyFormat["PostcodeExtendedLow"] = zipExtended

        address_payload = {
            "XAVRequest": {
                "AddressKeyFormat": addressKeyFormat
            }
        }

        response = requests.post(url, headers=headers, params=query, json=address_payload)

        if response.status_code != 200:
            raise ValueError(f"Error validating address: {response.status_code} {response.text}")

        response = response.text

        return str(response)

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