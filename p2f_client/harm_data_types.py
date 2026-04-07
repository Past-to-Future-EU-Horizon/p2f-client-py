# Local libraries
from p2f_pydantic.harm_data_types import HARM_Data_Type
from .conn import health_check
# Third Party Libraries
import requests
from furl import furl
# Batteries included libraries
from uuid import UUID
from typing import Optional, List

class harm_data_type:
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "harm-data-types/"
        self.hdt_url = self.base_url / self.prefix
        self.harm_data_types_queue = []
    def add_harm_data_type(self, new_data_type: HARM_Data_Type):
        self.harm_data_types_queue.append(new_data_type)
    def upload_data_types(self):
        if health_check(self.base_url):
            for datatype in self.harm_data_types_queue:
                r = requests.post(self.hdt_url, 
                                  data=self.p2fclient.json_serialize_with_auth("new_harm_data_type", datatype.model_dump_json(exclude_unset=True)),
                            headers={"Content-Type": "application/json"})
    def upload_data_type(self, new_data_type: HARM_Data_Type):
        if health_check(self.base_url):
            r = requests.post(self.hdt_url, 
                              data=self.p2fclient.json_serialize_with_auth("new_harm_data_type", new_data_type.model_dump_json(exclude_unset=True)),
                            headers={"Content-Type": "application/json"})
            return HARM_Data_Type(**r.json())
    def list_data_types(self, 
                        measure: Optional[str]=None,
                        unit_of_measure: Optional[str]=None,
                        method: Optional[str]=None, 
                        dataset_id: Optional[UUID]=None):
        params = {"measure": measure,
                  "unit_of_measure": unit_of_measure,
                  "method": method, 
                  "dataset_id": dataset_id}
        params = {x:y for x, y in params.items() if y != None}
        if health_check(self.base_url):
            r = requests.get(self.hdt_url,
                            params=params, 
                            data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
            return [HARM_Data_Type(**x) for x in r.json()]
    def get_data_type(self, datatype_id: UUID):
        if health_check(self.base_url):
            r = requests.get(self.hdt_url / datatype_id, 
                             data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
            return HARM_Data_Type(**r.json())
    def delete_data_type(self, datatype_id: UUID):
        if health_check(self.base_url):
            r = requests.delete(self.hdt_url / datatype_id, 
                                data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})