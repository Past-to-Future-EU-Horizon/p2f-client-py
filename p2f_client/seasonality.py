# Local libraries
from p2f_pydantic.seasonality import Seasonality_DS
from .conn import health_check
# Third Party Libraries
import requests
# Batteries included libraries
from uuid import UUID
from typing import Optional, List
from json import loads

class seasonality:
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "seasonality/"
        self.seasonality_url = self.base_url / self.prefix
        self.data_model = Seasonality_DS
    def add_seasonality(self, 
                   dataset_id: UUID, 
                   new_seasonality: Seasonality_DS):
        if health_check(self.base_url):
            local_url = self.seasonality_url / dataset_id
            r = requests.post(local_url, 
                              headers=self.p2fclient.base_headers, 
                              data=new_seasonality.model_dump_json(exclude_unset=True))
    def get_season(self, 
                   dataset_id: UUID) -> Seasonality_DS:
        if health_check(self.base_url):
            local_url = self.seasonality_url / dataset_id
            r = requests.get(local_url, 
                             headers=self.p2fclient.base_headers)
            return Seasonality_DS(**r.json())
    def delete_season(self, 
                      dataset_id: UUID):
        if health_check(self.base_url):
            local_url = self.seasonality_url / dataset_id
            r = requests.delete(local_url, 
                                headers=self.p2fclient.base_headers)