# Local libraries
from p2f_pydantic.harm_reference import HARM_Reference
from .conn import health_check
# Third Party Libraries
import requests
# Batteries included libraries
from typing import Optional, List
from uuid import UUID

class harm_reference:
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "harm-reference/"
        self.hr_url = self.base_url / self.prefix
        self.harmonized_reference_queue = []
    def add_harm_reference(self, new_reference: HARM_Reference):
        self.harmonized_reference_queue.append(new_reference)
    def upload_harm_reference_queue(self) -> List[HARM_Reference]:
        inserted_harm_references = []
        if health_check(self.base_url):
            for ref in self.harmonized_reference_queue:
                r = requests.post(self.hr_url, data=self.p2fclient.json_serialize_with_auth("new_reference", ref.model_dump_json(exclude_unset=True)),
                            headers={"Content-Type": "application/json"})
                inserted_harm_references.append(HARM_Reference(**r.json()))
            return inserted_harm_references
    def upload_harm_reference(self, new_reference: HARM_Reference) -> HARM_Reference:
        if health_check(self.base_url):
            r = requests.post(self.hr_url, data=self.p2fclient.json_serialize_with_auth("new_reference", new_reference.model_dump_json(exclude_unset=True)),
                            headers={"Content-Type": "application/json"})
            if r.ok:
                return (HARM_Reference(**r.json()))
    def list_harm_references(self) -> List[HARM_Reference]:
        if health_check(self.base_url):
            r = requests.get(self.hr_url, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
            if r.ok:
                return [HARM_Reference(**x) for x in r.json()]
            else:
                return []
    def get_harm_reference(self, reference_id: UUID) -> HARM_Reference:
        if health_check(self.base_url):
            r = requests.get(self.hr_url / reference_id, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
            if r.ok:
                return HARM_Reference(**r.json())
    def delete_harm_reference(self, reference_id: UUID):
        if health_check(self.base_url):
            r = requests.delete(self, reference_id, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
    def assign_harm_reference(self, 
                              reference_id: UUID, 
                              record_hash: str):
        assign_url = self.hr_url
        assign_url.args["reference_id"] = reference_id
        assign_url.args["record_hash"] = record_hash
        if health_check(self.base_url):
            r = requests.post(assign_url, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
    def remove_harm_reference(self, 
                              reference_id: UUID, 
                              record_hash: str):
        assign_url = self.hr_url
        assign_url.args["reference_id"] = reference_id
        assign_url.args["record_hash"] = record_hash
        if health_check(self.base_url):
            r = requests.delete(assign_url, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})