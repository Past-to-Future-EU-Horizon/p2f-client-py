# Local libraries
from p2f_pydantic.harm_reference import harm_reference as Harm_reference
from .p2f_client import P2F_Client
from .conn import health_check
# Third Party Libraries
import requests
# Batteries included libraries
from typing import Optional, List
from uuid import UUID

class harm_reference:
    def __init__(self, p2fclient: P2F_Client):
        self.base_url = p2fclient.base_url
        self.prefix = "harm-reference"
        self.hr_url = self.base_url / self.prefix
        self.harmonized_reference_queue = []
    def add_harm_reference(self, new_reference: Harm_reference):
        self.harmonized_reference_queue.append(new_reference)
    def upload_harm_reference_queue(self) -> List[Harm_reference]:
        inserted_harm_references = []
        if health_check(self.base_url):
            for ref in self.harmonized_reference_queue:
                r = requests.post(self.hr_url, 
                                data=ref.model_dump_json(exclude_unset=True))
                inserted_harm_references.append(Harm_reference(**r.json()))
            return inserted_harm_references
    def upload_harm_reference(self, new_reference: Harm_reference) -> Harm_reference:
        if health_check(self.base_url):
            r = requests.post(self.hr_url, 
                            data=new_reference.model_dump_json(exclude_unset=True))
            if r.ok:
                return (Harm_reference(**r.json()))
    def list_harm_references(self) -> List[Harm_reference]:
        if health_check(self.base_url):
            r = requests.get(self.hr_url)
            if r.ok:
                return [Harm_reference(**x) for x in r.json()]
            else:
                return []
    def get_harm_reference(self, reference_id: UUID) -> Harm_reference:
        if health_check(self.base_url):
            r = requests.get(self.hr_url / reference_id)
            if r.ok:
                return Harm_reference(**r.json())
    def delete_harm_reference(self, reference_id: UUID):
        if health_check(self.base_url):
            r = requests.delete(self, reference_id)
    def assign_harm_reference(self, 
                              reference_id: UUID, 
                              record_hash: str):
        assign_url = self.hr_url
        assign_url.args["reference_id"] = reference_id
        assign_url.args["record_hash"] = record_hash
        if health_check(self.base_url):
            r = requests.post(assign_url)
    def remove_harm_reference(self, 
                              reference_id: UUID, 
                              record_hash: str):
        assign_url = self.hr_url
        assign_url.args["reference_id"] = reference_id
        assign_url.args["record_hash"] = record_hash
        if health_check(self.base_url):
            r = requests.delete(assign_url)