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
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Optional


class P2F_Client:
    def __init__(self, 
                 hostname: str, 
                 port: int=443, 
                 https: bool=True, 
                 email: Optional[str]=None, 
                 token: Optional[str] = None, 
                 token_expiration: Optional[datetime]=None):
        self.version = (0, 0, 7) # turn this into a real named tuple one day
        self.hostname = hostname
        self.port = port
        if https:
            self.protocol = "https"
        else:
            self.protocol = "http"
        self.host_url = f"{self.protocol}://{self.hostname}:{self.port}"
        self.base_url = furl.furl(self.host_url)
        self.email= email
        self.token = token
        if self.token is not None:
            if token_expiration is None:
                # It's not true, but it does inform us that the token could possibly last till tomorrow
                self.TOKEN_EXPIRATION = datetime.now(tz=ZoneInfo("UTC")) + timedelta(hours=24)
                raise UserWarning("A generic token expiration time was used, the token could expire sooner than the currently set token expiration time")
            else: 
                self.TOKEN_EXPIRATION = token_expiration
        self.child_class_loading()
    def child_class_loading(self):
        # Separated this out so we can reload it later. 
        self.datasets = datasets(self)
        self.harm_data_records = harm_data_records(self)
        self.harm_data_type = harm_data_type(self)
        self.harm_numerical = harm_numerical(self)
        self.harm_location = harm_location(self)
        self.harm_species = harm_species(self)
        self.harm_timeslice = harm_timeslice(self)
        self.harm_reference = harm_reference(self)
    def request_token(self):
        # self.email = email
        self.token_url = self.base_url / "token"
        self.token_request_url = self.token_url / "request"
        token_request_model = Temp_Account(email=self.email)
        # calculate the datetime of the token before making the request
        #    so that our expiration time is just before actual expiration. 
        self.TOKEN_EXPIRATION = datetime.now(tz=ZoneInfo("UTC")) + timedelta(hours=24)
        if health_check(self.base_url):
            r = requests.post(self.token_request_url, data=token_request_model.model_dump_json(exclude_unset=True))
            print(r.json())
    def set_token(self, token: str):
        self.token = token
        self.temp_account = Temp_Account(email=self.email, token=self.token)
        # reload the child classes so they will have the token
        self.child_class_loading()
    def json_serialize_with_auth(self, label: str, json: str):
        return f"""{{"auth":{self.temp_account.model_dump_json(exclude_unset=True)},{label}:{json}}}"""