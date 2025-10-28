# Local libraries
from .datasets import datasets
# Third Party Libraries
import requests
import furl
# Batteries included libraries

class P2F_Client:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.host_url = f"https://{self.hostname}:{self.port}"
        self.base_url = furl.furl(self.host_url)
        self.datasets = datasets(self.base_url)
    def request_token(self, email):
        self.email = email