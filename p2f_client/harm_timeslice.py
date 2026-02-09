# Local libraries
from p2f_pydantic.harm_timeslices import harm_timeslice as Harm_timeslice
# Third Party Libraries
import requests
# Batteries included libraries
from uuid import UUID
from typing import Optional, List

class harm_timeslice:
    def __init__(self, base_url):
        self.base_url = base_url
        self.prefix = "harm-timeslice"
        self.ht_url = self.base_url / self.prefix
        self.harmonized_timeslice_queue = []
    def add_timeslice(self, new_timeslice: Harm_timeslice):
        self.harmonized_timeslice_queue.append(new_timeslice)
    def upload_timeslice_queue(self):
        inserted_timeslice_list = []
        for timeslice in self.harmonized_timeslice_queue:
            r = requests.post(self.ht_url, 
                              data=timeslice.model_dump_json(exclude_unset=True))
            inserted_timeslice_list.append(Harm_timeslice(**r.json()))
        return inserted_timeslice_list
    def upload_timeslice(self, new_timeslice: Harm_timeslice) -> Harm_timeslice:
        r = requests.post(self.ht_url, 
                          data=new_timeslice.model_dump_json(exclude_unset=True))
        return Harm_timeslice(**r.json())
    def list_timeslices(self,
                        named_time_period: Optional[str]=None, 
                        older_search_age: Optional[int]=None,
                        recent_search_age: Optional[int]=None,) -> List[Harm_timeslice]:
        params = {"named_time_period": named_time_period,
                  "older_search_age": older_search_age,
                  "recent_search_age": recent_search_age}
        params = {x: y for x, y in params.items() if y != None}
        r = requests.get(self.ht_url, 
                         params=params)
        return [Harm_timeslice(**x) for x in r.json()]
    def get_timeslice(self, 
                      timeslice_id: UUID) -> Harm_timeslice:
        r = requests.get(self.ht_url / timeslice_id)
        return Harm_timeslice(**r.json())
    def delete_timeslice(self, 
                         timeslice_id: UUID) -> Harm_timeslice:
        r = requests.delete(self.ht_url / timeslice_id)
    def assign_timeslice(self, 
                         timeslice_id: UUID, 
                         record_hash: str):
        assign_url = self.ht_url / "assign"
        assign_url.args["timeslice_id"] = timeslice_id
        assign_url.args["record_hash"] = record_hash
        r = requests.post(assign_url)
    def remove_timeslice(self, 
                         timeslice_id: UUID, 
                         record_hash: str):
        remove_url = self.ht_url / "remove"
        remove_url.args["timeslice_id"] = timeslice_id
        remove_url.args["record_hash"] = record_hash
        r = requests.delete(remove_url)