# Local libraries
from p2f_pydantic.harm_reference import HARM_Reference
from .conn import health_check
# Third Party Libraries
import requests
# Batteries included libraries
from typing import Optional, List
from uuid import UUID

class harm_reference:
    """Client library endpoint for interacting with the Harmonized Reference data model 
        on the P2F API
    """
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "harm-reference/"
        self.hr_url = self.base_url / self.prefix
        self.harmonized_reference_queue = []
    def upload_harm_reference(self, new_reference: HARM_Reference) -> HARM_Reference:
        """Upload a reference to the API directly

        :param new_reference: New reference to be uploaded to the API
        :type new_reference: HARM_Reference
        :return: The new reference as processed by the API
        :rtype: p2f_pydantic.harm_reference.HARM_Reference
        """
        if health_check(self.base_url):
            r = requests.post(self.hr_url, data=self.p2fclient.json_serialize_with_auth("new_reference", new_reference.model_dump_json(exclude_unset=True)),
                            headers={"Content-Type": "application/json"})
            if r.ok:
                return (HARM_Reference(**r.json()))
    def list_harm_references(self) -> List[HARM_Reference]:
        """List references that exist on the API. 

        In the future this function will have search parameters such as dataset_id and record_hash. 

        :return: A list of references from the API
        :rtype: List[p2f_pydantic.harm_reference.HARM_Reference]
        """
        if health_check(self.base_url):
            r = requests.get(self.hr_url, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
            if r.ok:
                return [HARM_Reference(**x) for x in r.json()]
            else:
                return []
    def get_harm_reference(self, reference_id: UUID) -> HARM_Reference:
        """Get an individual harm reference from the API by reference ID

        :param reference_id: Reference ID from the API
        :type reference_id: UUID
        :return: The reference from the API
        :rtype: p2f_pydantic.harm_reference.HARM_Reference
        """
        if health_check(self.base_url):
            r = requests.get(self.hr_url / reference_id, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
            if r.ok:
                return HARM_Reference(**r.json())
    def delete_harm_reference(self, reference_id: UUID):
        """Not implemented

        :param reference_id: Delete a reference from the API based on the reference ID
        :type reference_id: UUID
        """
        if health_check(self.base_url):
            r = requests.delete(self, reference_id, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
    def assign_harm_reference(self, 
                              reference_id: UUID, 
                              record_hash: str):
        """Assign a harm reference to a record hash

        :param reference_id: reference id from the API
        :type reference_id: UUID
        :param record_hash: record_hash from the API
        :type record_hash: str
        """
        assign_url = self.hr_url / "assign"
        assign_url.args["reference_id"] = reference_id
        assign_url.args["record_hash"] = record_hash
        if health_check(self.base_url):
            r = requests.post(assign_url, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
    def remove_harm_reference(self, 
                              reference_id: UUID, 
                              record_hash: str):
        """Not implemented

        :param reference_id: Reference ID from the API
        :type reference_id: UUID
        :param record_hash: Record hash from the API
        :type record_hash: str
        """
        remove_url = self.hr_url / "remove"
        remove_url.args["reference_id"] = reference_id
        remove_url.args["record_hash"] = record_hash
        if health_check(self.base_url):
            r = requests.delete(remove_url, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})