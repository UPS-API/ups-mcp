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

Environment variables will be loaded from a .env file in the project's root directory.

**Execution**

You can run the package using uvx:

```uvx --from git+https://github.com/UPS-API/ups-mcp ups-mcp```


## Popular Integrations
Here is the config file that works with VS Code, and other MCP Clients 
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

UPS MCP server is still in active development. More tools coming soon!
