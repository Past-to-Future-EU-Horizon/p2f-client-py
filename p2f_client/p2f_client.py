# Local libraries
from .datasets import datasets
# Third Party Libraries
import requests
# Batteries included libraries

class P2F_Client:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.host_url = f"https://{self.hostname}:{self.port}"
        self.datasets = datasets(self.host_url)