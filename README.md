# UPS MCP Server
A Model Context Protocol (MCP) server for UPS shipping and logistics capabilities. This server enables AI systems to seamlessly integrate with UPS API tools. 

Users can integrate with the MCP server to allow AI agents to facilitate tracking events on their behalf, including tracking the status of a shipment, the latest transit screen, and expected delivery date and time. Agents will be authenticated using OAuth client credentials provided by the user after application creation on the UPS Developer Portal.  

## Usage
**Prerequisites**
- Obtain a Client ID and Client Secret: Create an application on the UPS Developer Portal to obtain your OAuth credentials – Client ID and Client Secret. (https://developer.ups.com/get-started?loc=en_US)
- Python 3.12 or higher
- Install uv (Python Package)

**Environment Variables**
- ```CLIENT_ID``` - UPS Client ID
- ```CLIENT_SECRET``` - UPS Client Secret
- ```ENVIRONMENT``` - Whether to point to Test (CIE) or Production (Accepted values: test, production)

**Execution**

You can run the package using uvx:

```uvx --from git+https://github.com/UPS-API/ups-mcp ups-mcp```

**Note**: Your API credentials are sensitive. Do not commit them to version control. We recommend managing secrets securely using GitHub Secrets, a vault, or a password manager.

## Popular Integrations
Here is the sample config file, different MCP Clients may require modification.
```json
{
  "mcpServers": {
    "ups-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "git+https://github.com/UPS-API/ups-mcp", "ups-mcp"],
      "env": {
        "CLIENT_ID": "**********",
        "CLIENT_SECRET": "**********",
        "ENVIRONMENT": "test"
      }
    }
  }
}
```

## Available Tools


- ```track_package```: Track a package using the UPS Tracking API
    
    Args:
     - inquiryNumber (str): the unique package identifier. Each inquiry number must be between 7 and 34 characters in length. Required.
    - locale (str): Language and country code of the user, separated by an underscore. Default value is 'en_US'. Not required.
    - returnSignature (bool): a boolean to indicate whether a signature is required, default is false. Not required.
    - returnMilestones (bool): a boolean to indicate whether detailed information on a package's movements is required, default is false. Not required
    - returnPOD (bool): a boolean to indicate whether a proof of delivery is required, default is false. Not required

    Returns:
    - str: The response from the tracking capability, this is a string of json tracking data.
- ```validate_address```: Validate an address using the UPS Address Validation API for the U.S. or Puerto Rico
    
    Args:
     - addressLine1 (str): The primary address details including the house or building number and the street name, e.g. 123 Main St. Required.
     - addressLine2 (str): Additional information like apartment or suite numbers, e.g. Apt 4B. Not required.
    - politicalDivision1 (str): The two-letter state or province code, e.g. GA for Georgia. Required.
    - politicalDivision2 (str): The city or town name, e.g. Springfield. Required.
    - zipPrimary (str): The postal code. Required.
    - zipExtended (str): 4 digit Postal Code extension. For US use only. Not required.
    - urbanization (str): Puerto Rico Political Division 3. Only valid for Puerto Rico. Not required.
    - countryCode (str): The country code, e.g. US. Required.

    Returns:
    - str: The json response body from the address validation API

UPS MCP server is still in active development. More tools coming soon!
