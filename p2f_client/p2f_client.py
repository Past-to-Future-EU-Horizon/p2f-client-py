# Local libraries
from .datasets import datasets
from .harm_data_record import harm_data_records
from .harm_data_types import harm_data_type
from .harm_numerical import harm_numerical
from .harm_location import harm_location
from .harm_species import harm_species
from .harm_timeslice import harm_timeslice
from .harm_reference import harm_reference
from .conn import health_check
from p2f_pydantic.temp_accounts import Temp_Account
# Third Party Libraries
import requests
import furl
# Batteries included libraries
from datetime import datetime
from zoneinfo import ZoneInfo


class P2F_Client:
    def __init__(self, hostname, port: int=443, https: bool=True):
        self.version = (0, 0, 3) # turn this into a real named tuple one day
        self.hostname = hostname
        self.port = port
        if https:
            self.protocol = "https"
        else:
            self.protocol = "http"
        self.host_url = f"{self.protocol}://{self.hostname}:{self.port}"
        self.base_url = furl.furl(self.host_url)
        self.datasets = datasets(self.base_url)
        self.child_class_loading()
    def child_class_loading(self):
        # Separated this out so we can reload it later. 
        self.harm_data_records = harm_data_records(self)
        self.harm_data_type = harm_data_type(self)
        self.harm_numerical = harm_numerical(self)
        self.harm_location = harm_location(self)
        self.harm_species = harm_species(self)
        self.harm_timeslice = harm_timeslice(self)
        self.harm_reference = harm_reference(self)
    def request_token(self, email):
        self.email = email
        self.token_url = self.host_url / "token"
        self.token_request_url = self.token_url / "request"
        token_request_model = Temp_Account(email=email)
        # calculate the datetime of the token before making the request
        #    so that our expiration time is just before actual expiration. 
        self.TOKEN_EXPIRATION = datetime.now(tz=ZoneInfo("UTC"))
        if health_check(self.base_url):
            r = requests.post(self.token_request_url, data=token_request_model.model_dump_json(exclude_unset=True))
            print(r.json())
    def set_token(self, token: str):
        self.token = token
        # reload the child classes so they will have the token
        self.child_class_loading()