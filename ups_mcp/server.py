from typing import Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
from . import tools
from . import constants

# Initialize FastMCP server
mcp = FastMCP("ups-mcp")

# Initialize tool manager
load_dotenv()
if os.getenv("ENVIRONMENT") == "production":
    base_url = constants.PRODUCTION_URL
else:
    base_url = constants.CIE_URL

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

tool_manager = tools.ToolManager(base_url=base_url, client_id=client_id, client_secret=client_secret)

@mcp.tool()
async def track_package(inquiryNumber: str, locale:str="en_US", returnSignature:bool=False, returnMilestones:bool=False, returnPOD:bool=False) -> str:
    """
    The Track API retrieves current status of shipments such as Small Package 1Z, Infonotice, Mail Innovations, FGV, or UPS Freight shipments
    using the inquiry number. The tracking response data typically includes package movements/activities, destination UPS access point
    information, expected delivery dates/times, etc. The response returns an array of shipment objects containing detailed tracking information 
    and status for the package(s) associated with the inquiryNumber, including current status, activity history, delivery details, package details, and more.
    
    Args:
        inquiryNumber (str): the unique package identifier. Each inquiry number must be between 7 and 34 characters in length. Required.
        locale (str): Language and country code of the user, separated by an underscore. Default value is 'en_US'. Not required.
        returnSignature (bool): a boolean to indicate whether a signature is required, default is false. Not required.
        returnMilestones (bool): a boolean to indicate whether detailed information on a package's movements is required, default is false. Not required
        returnPOD (bool): a boolean to indicate whether a proof of delivery is required, default is false. Not required

    Returns:
        str: The response from the tracking capability, this is a string of json tracking data.
    """
    tracking_data = tool_manager.track_package(inquiryNum=inquiryNumber, locale=locale, returnSignature=returnSignature, returnMilestones=returnMilestones, returnPOD=returnPOD)

    return tracking_data

@mcp.tool()
async def validate_address(addressLine1: str, politicalDivision1: str, politicalDivision2: str, zipPrimary: str, countryCode: str, addressLine2: str="", urbanization: str="", zipExtended: str="") -> str:
    """
    Checks addresses against the United States Postal Service database of valid addresses in the U.S. and Puerto Rico.

    Args:
        addressLine1 (str): The primary address details including the house or building number and the street name, e.g. 123 Main St. Required.
        addressLine2 (str): Additional information like apartment or suite numbers. E.g. Apt 4B. Optional.
        politicalDivision1 (str): The two-letter state or province code e.g. GA for Georgia. Required.
        politicalDivision2 (str): The city or town name, e.g. Springfield. Required.
        zipPrimary (str): The postal code. Required.
        zipExtended (str): 4 digit Postal Code extension. For US use only. Optional.
        urbanization (str): Puerto Rico Political Division 3. Only valid for Puerto Rico. Optional.
        countryCode (str): The country code, e.g. US. Required.

    Returns:
        str: A JSON response containing address validation results. The response includes one of three indicators:
        - ValidAddressIndicator: Address is valid. Contains a 'Candidate' object with the corrected/standardized address including normalized formatting, corrected ZIP codes, and ZIP+4 extensions.
        - AmbiguousAddressIndicator: Multiple possible address matches found. Review candidates to select the correct address.
        - NoCandidatesIndicator: Address could not be validated or does not exist in the USPS database.
    """
    validation_data = tool_manager.validate_address(addressLine1=addressLine1, addressLine2=addressLine2, politicalDivision1=politicalDivision1, politicalDivision2=politicalDivision2, zipPrimary=zipPrimary, zipExtended=zipExtended, urbanization=urbanization, countryCode=countryCode)

    return validation_data

def main():
    print("Starting UPS MCP Server...")
    try:
        mcp.run(transport='stdio')
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()