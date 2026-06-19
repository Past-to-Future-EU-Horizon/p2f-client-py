# Local libraries
from .datasets import datasets
from .harm_data_record import harm_data_records
from .harm_data_types import harm_data_type
from .harm_numerical import harm_numerical
from .harm_location import harm_location
from .harm_species import harm_species
from .harm_timeslice import harm_timeslice
from .harm_reference import harm_reference
from .harm_age import harm_age
from .link_git import git
from .keywords import keywords
from .season import season
from .seasonality import seasonality
from .conn import health_check
from p2f_pydantic.temp_accounts import Temp_Account
from p2f_pydantic.system import API_Metadata, Semantic_Version
# Third Party Libraries
import requests
import furl
# Batteries included libraries
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Optional


class P2F_Client:
    """Base P2F Client class that initializes all interactions with the P2F API
    """
    def __init__(self, 
                 hostname: str, 
                 port: int=443, 
                 https: bool=True,
                 email: Optional[str]=None, 
                 token: Optional[str]=None):
        """Initializer for the P2F Client library

        :param hostname: string representing the hostname of the API
        :type hostname: str
        :param port: integer of the API port, defaults to 443
        :type port: int, optional
        :param https: boolean of whether to use HTTPS (True) or HTTP (False), defaults to True
        :type https: bool, optional
        :param email: email address of the client that will interact with the API, defaults to None
        :type email: Optional[str], optional
        """
        self.version = Semantic_Version(major=0, minor=0, patch=25)
        self.hostname = hostname
        self.port = port
        if https:
            self.protocol = "https"
        else:
            self.protocol = "http"
        self.host_url = f"{self.protocol}://{self.hostname}:{self.port}"
        self.base_url = furl.furl(self.host_url)
        self.auth_email = email
        self.auth_token = token
        self.probe_api_endpoint()
        self.base_headers = {"Accept": "application/json", 
                             "Content-Type": "application/json", 
                             "x-p2f-token": self.auth_token,
                             "x-p2f-email": self.auth_email}
        self.child_class_loading()
        
    def probe_api_endpoint(self):
        """Function to get metadata about the configured API.

        :raises EnvironmentError: If the client library is a major version behind the API's minimum 
            supported major version. 
        :raises RuntimeWarning: If the client library is a minor version behind the API's minimum 
            upported minor version. 
        :raises RuntimeWarning: If the client library is a patch version behind the API's minimum 
            supported patch version. 
        """
        if health_check(self.base_url):
            r = requests.get(self.base_url / "version")
            if r.ok:
                api_meta = API_Metadata(**r.json())
                if api_meta.pyclient_minimum_version.major > self.version.major:
                    raise EnvironmentError("Current p2f-client-py version does not match API server's minimum supported version. Update your p2f-client-py library.")
                else:
                    if api_meta.pyclient_minimum_version.minor > self.version.minor:
                        raise RuntimeWarning("The minor version of this library, p2f-client-py, is less than the minimum supported minor version of the API server. You may experience errors when interacting with the API through the client. Please update p2f-client-py")
                    else:
                        if api_meta.pyclient_minimum_version.patch > self.version.patch:
                            raise RuntimeWarning("The patch version of this library, p2f-client-py, is less than the minimum supported patch version of the API server. You should not, but may experience errors when interacting with the API through the client. Please update p2f-client-py")
    def child_class_loading(self):
        """A function to reload the child data classes for interacting with specific API components."""
        # Separated this out so we can reload it later. 
        self.base_headers = {"Accept": "application/json", 
                             "Content-Type": "application/json", 
                             "x-p2f-token": self.auth_token,
                             "x-p2f-email": self.auth_email}
        self.datasets = datasets(self)
        self.harm_data_records = harm_data_records(self)
        self.harm_data_type = harm_data_type(self)
        self.harm_numerical = harm_numerical(self)
        self.harm_location = harm_location(self)
        self.harm_species = harm_species(self)
        self.harm_timeslice = harm_timeslice(self)
        self.harm_reference = harm_reference(self)
        self.harm_age = harm_age(self)
        self.link_git = git(self)
        self.keywords = keywords(self)
        self.season = season(self)
        self.seasonality = seasonality(self)
    def request_token(self):
        """Sends a requst to the API to request an API token through email. 
            If the client library does not have an email address currently configured
                it will request an email address from the user. 
            An email address is required for all practical uses of the API. """
        self.token_url = self.base_url / "token"
        self.token_request_url = self.token_url / "request"
        token_request_model = Temp_Account(email=self.auth_email)
        # calculate the datetime of the token before making the request
        #    so that our expiration time is just before actual expiration. 
        self.auth_token_expiration = datetime.now(tz=ZoneInfo("UTC")) + timedelta(hours=24)
        if health_check(self.base_url):
            r = requests.post(self.token_request_url, 
                              data=token_request_model.model_dump_json(exclude_unset=True),
                              headers=self.base_headers)
            print(r.json())
    def set_token(self, token):
        self.auth_token = token
        self.child_class_loading()