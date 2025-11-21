# Local libraries
from .datasets import datasets
from .harm_data_record import harm_data_records
from .harm_data_types import harm_data_type
from .harm_numerical import harm_numerical
from .harm_location import harm_location
# Third Party Libraries
import requests
import furl
# Batteries included libraries

class P2F_Client:
    def __init__(self, hostname, port: int=443, https: bool=True):
        self.hostname = hostname
        self.port = port
        if https:
            self.protocol = "https"
        else:
            self.protocol = "http"
        self.host_url = f"{self.protocol}://{self.hostname}:{self.port}"
        self.base_url = furl.furl(self.host_url)
        self.datasets = datasets(self.base_url)
        self.harm_data_records = harm_data_records(self.base_url)
        self.harm_data_type = harm_data_type(self.base_url)
        self.harm_numerical = harm_numerical(self.base_url)
        self.harm_location = harm_location(self.base_url)
    def request_token(self, email):
        self.email = email
        self.token_url = self.host_url / "nov-2025-congress"
        self.token_request_url = self.token_url / "request"
        r = requests.post(self.token_request_url, data={"email": email})
        print(r.json())
    def set_token(self, token):
        self.token = token