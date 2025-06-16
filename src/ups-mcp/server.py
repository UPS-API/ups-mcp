from typing import Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import tools

# Initialize FastMCP server
mcp = FastMCP("ups-mcp")

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
    if not inquiryNumber:
        return "Invalid Inquiry Number, try again"
    
    try:
        tracking_data = tools.track_package(inquiryNum=inquiryNumber, locale=locale, returnSignature=returnSignature, returnMilestones=returnMilestones, returnPOD=returnPOD)
    except Exception as e:
        return f"An error occurred while tracking the package: {str(e)}"

    return tracking_data

def main():
    #load_dotenv()
    mcp.run(transport='stdio')

if __name__ == "__main__":
    print("Starting UPS MCP Server...")
    main()