# Local libraries
from p2f_pydantic.seasonality import Season
from .conn import health_check
# Third Party Libraries
import requests
# Batteries included libraries
from uuid import UUID
from typing import Optional, List
from json import loads

class season:
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "season/"
        self.season_url = self.base_url / self.prefix
        self.data_model = Season
    def add_season(self, 
                   record_hash: str, 
                   new_season: Season):
        if health_check(self.base_url):
            local_url = self.season_url / record_hash
            r = requests.post(local_url, 
                              headers=self.p2fclient.base_headers, 
                              data=new_season.model_dump_json(exclude_unset=True))
    def get_season(self, 
                   record_hash: str) -> Season:
        if health_check(self.base_url):
            local_url = self.season_url / record_hash
            r = requests.get(local_url, 
                             headers=self.p2fclient.base_headers)
            return Season(**r.json())
    def delete_season(self, 
                   record_hash: str):
        if health_check(self.base_url):
            local_url = self.season_url / record_hash
            r = requests.delete(local_url, 
                                headers=self.p2fclient.base_headers)