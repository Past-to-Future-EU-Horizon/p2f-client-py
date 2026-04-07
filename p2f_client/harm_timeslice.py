# Local libraries
from p2f_pydantic.harm_timeslices import HARM_Timeslice
from .conn import health_check
# Third Party Libraries
import requests
# Batteries included libraries
from uuid import UUID
from typing import Optional, List

class harm_timeslice:
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "harm-timeslice/"
        self.ht_url = self.base_url / self.prefix
        self.harmonized_timeslice_queue = []
    def add_timeslice(self, new_timeslice: HARM_Timeslice):
        self.harmonized_timeslice_queue.append(new_timeslice)
    def upload_timeslice_queue(self):
        inserted_timeslice_list = []
        if health_check(self.base_url):
            for timeslice in self.harmonized_timeslice_queue:
                r = requests.post(self.ht_url, 
                                  data=self.p2fclient.json_serialize_with_auth("new_harm_timeslice", timeslice.model_dump_json(exclude_unset=True)),
                            headers={"Content-Type": "application/json"})
                inserted_timeslice_list.append(HARM_Timeslice(**r.json()))
            return inserted_timeslice_list
    def upload_timeslice(self, new_timeslice: HARM_Timeslice) -> HARM_Timeslice:
        if health_check(self.base_url):
            r = requests.post(self.ht_url, 
                              data=self.p2fclient.json_serialize_with_auth("new_harm_timeslice", new_timeslice.model_dump_json(exclude_unset=True)),
                            headers={"Content-Type": "application/json"})
            return HARM_Timeslice(**r.json())
    def list_timeslices(self,
                        named_time_period: Optional[str]=None, 
                        older_search_age: Optional[int]=None,
                        recent_search_age: Optional[int]=None,) -> List[HARM_Timeslice]:
        params = {"named_time_period": named_time_period,
                  "older_search_age": older_search_age,
                  "recent_search_age": recent_search_age}
        params = {x: y for x, y in params.items() if y != None}
        if health_check(self.base_url):
            r = requests.get(self.ht_url, 
                            params=params, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
            return [HARM_Timeslice(**x) for x in r.json()]
    def get_timeslice(self, 
                      timeslice_id: UUID) -> HARM_Timeslice:
        if health_check(self.base_url):
            r = requests.get(self.ht_url / timeslice_id, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
            return HARM_Timeslice(**r.json())
    def delete_timeslice(self, 
                         timeslice_id: UUID) -> HARM_Timeslice:
        if health_check(self.base_url):
            r = requests.delete(self.ht_url / timeslice_id, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
    def assign_timeslice(self, 
                         timeslice_id: UUID, 
                         record_hash: str):
        assign_url = self.ht_url / "assign"
        assign_url.args["timeslice_id"] = timeslice_id
        assign_url.args["record_hash"] = record_hash
        if health_check(self.base_url):
            r = requests.post(assign_url, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
    def remove_timeslice(self, 
                         timeslice_id: UUID, 
                         record_hash: str):
        remove_url = self.ht_url / "remove"
        remove_url.args["timeslice_id"] = timeslice_id
        remove_url.args["record_hash"] = record_hash
        if health_check(self.base_url):
            r = requests.delete(remove_url, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})