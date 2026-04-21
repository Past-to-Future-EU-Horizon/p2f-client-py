# Local libraries
from p2f_pydantic.harm_timeslices import HARM_Timeslice
from .conn import health_check
# Third Party Libraries
import requests
# Batteries included libraries
from uuid import UUID
from typing import Optional, List

class harm_timeslice:
    """Class to interact with HARM Timeslices on the API
    """
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "harm-timeslice/"
        self.ht_url = self.base_url / self.prefix
        self.data_model = HARM_Timeslice
    def upload_timeslice(self, new_timeslice: HARM_Timeslice) -> HARM_Timeslice:
        """Upload a timeslice directly to the P2F API. 

        :param new_timeslice: New timeslice to add to the API
        :type new_timeslice: p2f_pydantic.harm_timeslices.HARM_Timeslice
        :return: HARM_Timeslice as processed by the API
        :rtype: p2f_pydantic.harm_timeslices.HARM_Timeslice
        """
        if health_check(self.base_url):
            r = requests.post(self.ht_url, 
                              data=self.p2fclient.jswa("new_harm_timeslice", new_timeslice.model_dump_json(exclude_unset=True)),
                            headers={"Content-Type": "application/json"})
            return HARM_Timeslice(**r.json())
    def list_timeslices(self,
                        named_time_period: Optional[str]=None, 
                        older_search_age: Optional[int]=None,
                        recent_search_age: Optional[int]=None,) -> List[HARM_Timeslice]:
        """Retrieve a list of timeslices that exist on the P2F API

        :param named_time_period: A named time period that is agreed upon by the P2F Consortium, defaults to None
        :type named_time_period: Optional[str], optional
        :param older_search_age: The most distant time to search a timeslice by in years since present, defaults to None
        :type older_search_age: Optional[int], optional
        :param recent_search_age: The most recent time to search a timeslice by in years since present, defaults to None
        :type recent_search_age: Optional[int], optional
        :return: A list of timeslices
        :rtype: List[p2f_pydantic.harm_timeslices.HARM_Timeslice]
        """
        params = {"named_time_period": named_time_period,
                  "older_search_age": older_search_age,
                  "recent_search_age": recent_search_age}
        params = {x: y for x, y in params.items() if y != None}
        if health_check(self.base_url):
            r = requests.get(self.ht_url, 
                            params=params, data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})
            return [HARM_Timeslice(**x) for x in r.json()]
    def get_timeslice(self, 
                      timeslice_id: UUID) -> HARM_Timeslice:
        """Get an individual timeslice by its timeslice_id

        :param timeslice_id: ID of the timeslice on the API
        :type timeslice_id: UUID
        :return: retrieved timeslice from API
        :rtype: p2f_pydantic.harm_timeslices.HARM_Timeslice
        """
        if health_check(self.base_url):
            r = requests.get(self.ht_url / timeslice_id, data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})
            return HARM_Timeslice(**r.json())
    def delete_timeslice(self, 
                         timeslice_id: UUID):
        """Delete a timeslice from the API

        :param timeslice_id: timeslice_id from API
        :type timeslice_id: UUID
        """
        if health_check(self.base_url):
            r = requests.delete(self.ht_url / timeslice_id, data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})
    def assign_timeslice(self, 
                         timeslice_id: UUID, 
                         record_hash: str):
        """Assign a timeslice_id to a record hash on the API. 

        :param timeslice_id: Timeslice_id from the API
        :type timeslice_id: UUID
        :param record_hash: Record hash that exists in the API
        :type record_hash: str
        """
        assign_url = self.ht_url / "assign"
        assign_url.args["timeslice_id"] = timeslice_id
        assign_url.args["record_hash"] = record_hash
        if health_check(self.base_url):
            r = requests.post(assign_url, data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})
    def remove_timeslice(self, 
                         timeslice_id: UUID, 
                         record_hash: str):
        """Use this to remove an assigned timeslice from a record_hash. This does not delete the timeslice. 

        :param timeslice_id: Timeslice_id to be disassociated
        :type timeslice_id: UUID
        :param record_hash: Record hash to be disassociated
        :type record_hash: str
        """
        remove_url = self.ht_url / "remove"
        remove_url.args["timeslice_id"] = timeslice_id
        remove_url.args["record_hash"] = record_hash
        if health_check(self.base_url):
            r = requests.delete(remove_url, data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})