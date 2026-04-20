# p2f-client-py
Python client library for the Past to Future projects Portal. Past to Future is an EU Horizon funded project. 

## Installation

    pip install p2f-client-py


## Usage

Create a client

    from p2f_client import P2F_Client

    p2f_api_url = "{fill in API URL here}"
    port = 443

    client = P2F_Client(hostname=p2f_api_url, https=True, email="your@email.dm")

    # request a token
    client.request_token()

    # Open your local file and update the configuration with your new p2f token. 
    client.set_token()