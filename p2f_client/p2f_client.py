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
from p2f_pydantic.system import API_Metadata
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
        self.version = (0, 0, 13) # turn this into a real named tuple one day
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
            if self.email is not None:
                self.temp_account = Temp_Account(email=self.email, token=self.token)
        self.child_class_loading()
        self.probe_api_endpoint()
    def probe_api_endpoint(self):
        if health_check(self.base_url):
            r = requests.get(self.base_url / "version")
            if r.ok:
                api_meta = API_Metadata(**r.json())
                if api_meta.pyclient_minimum_version.major > self.version[0]:
                    raise EnvironmentError("Current p2f-client-py version does not match API server's minimum supported version. Update your p2f-client-py library.")
                else:
                    if api_meta.pyclient_minimum_version.minor > self.version[1]:
                        raise RuntimeWarning("The minor version of this library, p2f-client-py, is less than the minimum supported minor version of the API server. You may experience errors when interacting with the API through the client. Please update p2f-client-py")
                    else:
                        if api_meta.pyclient_minimum_version.patch > self.version[2]:
                            raise RuntimeWarning("The patch version of this library, p2f-client-py, is less than the minimum supported patch version of the API server. You should not, but may experience errors when interacting with the API through the client. Please update p2f-client-py")
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
            r = requests.post(self.token_request_url, 
                              data=token_request_model.model_dump_json(exclude_unset=True),
                              headers={"Content-Type": "application/json"})
            print(r.json())
    def set_token(self, token: str):
        self.token = token
        self.temp_account = Temp_Account(email=self.email, token=self.token)
        # reload the child classes so they will have the token
        self.child_class_loading()
    def json_serialize_with_auth(self, 
                                 label: Optional[str]=None, 
                                 JSON_str: Optional[str]=None):
        if label is not None:
            return f"""{{"auth":{self.temp_account.model_dump_json(exclude_unset=True)},"{label}":{JSON_str}}}"""
        if label is None:
            return self.temp_account.model_dump_json(exclude_unset=True)