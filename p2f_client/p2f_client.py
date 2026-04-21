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
from p2f_pydantic.system import API_Metadata, Semantic_Version
# Third Party Libraries
import requests
import furl
# Batteries included libraries
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Optional
import pathlib
from os import mkdir


class P2F_Client:
    """Base P2F Client class that initializes all interactions with the P2F API
    """
    def __init__(self, 
                 hostname: str, 
                 port: int=443, 
                 https: bool=True,
                 email: Optional[str]=None):
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
        self.version = Semantic_Version(major=0, minor=0, patch=16)
        self.hostname = hostname
        self.port = port
        if https:
            self.protocol = "https"
        else:
            self.protocol = "http"
        self.host_url = f"{self.protocol}://{self.hostname}:{self.port}"
        self.base_url = furl.furl(self.host_url)
        self.probe_api_endpoint()
        # DOT P2F File configuration
        self.dotp2f_init()
        self.dotp2f_folder_create()
        self.dotp2f_read_config()
        if self.auth_email == None and email == None:
            new_email = input("Please provide an email address: ")
            while new_email[0] in [" "]:
                new_email = new_email[1:]
            while new_email[-1] in [" ", "\n"]:
                new_email = new_email[:-1]
            self.auth_email = new_email
            self.dotp2f_update_config_parameter("EMAIL", new_email)
        elif self.auth_email == None and email is not None:
            self.auth_email = email
            self.dotp2f_update_config_parameter("EMAIL", new_email)
        if self.auth_token is None:
            if self.auth_token_expiration is None:
                if self.auth_email is not None:
                    run_token_request = input("No token or token expiration were found, would you like to request a new token now? (1) yes 2 no")
                    while run_token_request[-1] in [" ", "\n"]:
                        run_token_request = run_token_request[-1]
                    if run_token_request in (None, "1"):
                        self.request_token()
        if self.auth_token_expiration is not None:
            if self.auth_token_expiration < datetime.now(tz=ZoneInfo("UTC")):
                if self.auth_email is not None:
                    run_token_request = input("Your token is expired, would you like to request a new token now? (1) yes 2 no")
                    while run_token_request[-1] in [" ", "\n"]:
                        run_token_request = run_token_request[-1]
                    if run_token_request in (None, "1"):
                        self.request_token()
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
        self.datasets = datasets(self)
        self.harm_data_records = harm_data_records(self)
        self.harm_data_type = harm_data_type(self)
        self.harm_numerical = harm_numerical(self)
        self.harm_location = harm_location(self)
        self.harm_species = harm_species(self)
        self.harm_timeslice = harm_timeslice(self)
        self.harm_reference = harm_reference(self)
    def request_token(self):
        """Sends a requst to the API to request an API token through email. 
            If the client library does not have an email address currently configured
                it will request an email address from the user. 
            An email address is required for all practical uses of the API. """
        self.token_url = self.base_url / "token"
        self.token_request_url = self.token_url / "request"
        if self.auth_email is None:
            email = input("You have not set an email address, please set one now: ")
            while email[0] in [" "]:
                email = email[1:]
            while email[-1] in [" ", "\n"]:
                email = email[:-1]
            if len(email) > 0:
                if "@" in email: # This is not real validation, but it is something
                    self.dotp2f_update_config_parameter("EMAIL", email)
                    self.auth_email = email
                else:
                    raise ValueError("A valid email address was not provided")
            else: 
                raise ValueError("No email is set and no email was provided for input, cannot request a token. ")
        token_request_model = Temp_Account(email=self.auth_email)
        # calculate the datetime of the token before making the request
        #    so that our expiration time is just before actual expiration. 
        self.auth_token_expiration = datetime.now(tz=ZoneInfo("UTC")) + timedelta(hours=24)
        self.dotp2f_update_config_parameter("TOKEN_EXPIRATION", self.auth_token_expiration.strftime(self.dotp2f_datetime_template))
        self.dotp2f_update_config_parameter("TOKEN", "")
        if health_check(self.base_url):
            r = requests.post(self.token_request_url, 
                              data=token_request_model.model_dump_json(exclude_unset=True),
                              headers={"Content-Type": "application/json"})
            print(r.json())
    def set_token(self):
        """Reload the child classes once the token has been placed in the config file."""
        print(f"Please open the file {self.dotp2f_config} and paste your token from email into the TOKEN line of the file")
        token_confirm = input("When you have updated and saved the file, please enter a one (1) here: ")
        while token_confirm[0] in [" "]:
            token_confirm = token_confirm[1:]
        while token_confirm[-1] in [" ", "\n"]:
            token_confirm = token_confirm[:-1]
        if token_confirm in ["1", "one", "One", "ONE", "onE", "OnE", "oNE", "oNe"]:
            self.dotp2f_read_config()
            self.temp_account = Temp_Account(email=self.auth_email, token=self.auth_token)
            # reload the child classes so they will have the token
            self.child_class_loading()
        else:
            print("An irregular value was received, TOKEN WAS NOT LOADED FROM FILE. ")
    def json_serialize_with_auth(self, 
                                 label: Optional[str]=None, 
                                 JSON_str: Optional[str]=None):
        """Utility function that will run with all API calls to authenticate to the API"""
        if label is not None:
            return f"""{{"auth":{self.temp_account.model_dump_json(exclude_unset=True)},"{label}":{JSON_str}}}"""
        if label is None:
            return self.temp_account.model_dump_json(exclude_unset=True)
    def dotp2f_init(self):
        """Utility function to initialize the paths for the .p2f config file and folder"""
        self.dotp2f_datetime_template = "%Y-%m-%dT%H-%M-%SZ"
        home = pathlib.Path.home()
        self.dotp2f_dir = home / ".p2f"
        self.dotp2f_config = self.dotp2f_dir / "CONFIG"
    def dotp2f_folder_create(self):
        """Utility function to create .p2f folder and CONFIG file if they do not exist."""
        if self.dotp2f_dir.exists() == False:
            mkdir(self.dotp2f_dir)
        if self.dotp2f_config.exists() == False:
            with open(self.dotp2f_config, "w") as config_file:
                config_file.write("EMAIL = ''\n")
                config_file.write("TOKEN = ''\n")
                config_file.write("TOKEN_EXPIRATION = ''\n")
    def dotp2f_update_config_parameter(self, parameter: str, new_value: str):
        """Utility function to update a parameter in the .p2f/CONFIG file"""
        with open(self.dotp2f_config, "r") as config_read:
            lines = config_read.readlines()
        with open(self.dotp2f_config, "w") as config_write:
            for line in lines:
                if line.startswith(parameter): 
                    config_write.write(f"{parameter} = '{new_value}'\n")
                else:
                    config_write.write(line)
    def dotp2f_read_config(self):
        """Utility function to read the parameters from the .p2f/CONFIG file. """
        config = {}
        with open(self.dotp2f_config, "r") as config_read:
            for line in config_read.readlines():
                if "=" in line:
                    linesplit = line.split("=")
                    parameter = linesplit[0]
                    while parameter[0] in [" "]:
                        parameter = parameter[1:]
                    while parameter[-1] in [" ", "\n"]:
                        parameter = parameter[:-1]
                    read_value = linesplit[1]
                    read_value = read_value.split("'")[1]
                    config[parameter] = read_value
        if "EMAIL" in config.keys():
            if len(config["EMAIL"]) > 0:
                self.auth_email = config["EMAIL"]
            else:
                self.auth_email = None
        if "TOKEN_EXPIRATION" in config.keys():
            if len(config["TOKEN_EXPIRATION"]) > 0:
                auth_token_expiration = datetime.strptime(config["TOKEN_EXPIRATION"], self.dotp2f_datetime_template)
                self.auth_token_expiration = auth_token_expiration.replace(tzinfo=ZoneInfo("UTC"))
            else:
                self.auth_token_expiration = None
        if "TOKEN" in config.keys():
            if len(config["TOKEN"]) > 0:
                self.auth_token = config["TOKEN"]
                if self.auth_token_expiration is not None:
                    if datetime.now(tz=ZoneInfo("UTC")) > self.auth_token_expiration:
                        self.auth_token = None
                    else:
                        self.auth_token = config["TOKEN"]
                else:
                    self.auth_token = config["TOKEN"]
                    print("The token on file was found without an expiration, you may need to request a new token")
            else:
                self.auth_token = None