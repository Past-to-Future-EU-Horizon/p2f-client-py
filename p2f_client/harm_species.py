# Local libraries
from p2f_pydantic.harm_data_metadata import HARM_Data_Species
from .conn import health_check
# Third Party Libraries
import requests
# Batteries included libraries
from typing import Optional, List
from uuid import UUID

class harm_species:
    def __init__(self, p2fclient):
        self.base_url = p2fclient.base_url
        self.prefix = "harm-data-species"
        self.hds_url = self.base_url / self.prefix
        self.harmonized_species_queue = []
    def add_harm_species(self, new_species: HARM_Data_Species):
        self.harmonized_species_queue.append(new_species)
    def upload_harm_species_queue(self) -> List[HARM_Data_Species]:
        inserted_species = []
        if health_check(self.base_url):
            for record in self.harmonized_species_queue:
                r = requests.post(self.hds_url, data=record.model_dump_json(exclude_unset=True))
                inserted_species.append(HARM_Data_Species(**r.json()))
            return inserted_species
    def upload_harm_species(self, new_species: HARM_Data_Species):
        if health_check(self.base_url):
            r = requests.post(self.hds_url, 
                            data=new_species.model_dump_json(exclude_unset=True))
            return HARM_Data_Species(**r.json())
    def list_harm_species(self, 
                          tax_domain: Optional[str]=None,
                          tax_kingdom: Optional[str]=None,
                          tax_subkingdom: Optional[str]=None,
                          tax_infrakingdom: Optional[str]=None,
                          tax_phylum: Optional[str]=None,
                          tax_class: Optional[str]=None,
                          tax_subclass: Optional[str]=None,
                          tax_order: Optional[str]=None,
                          tax_suborder: Optional[str]=None,
                          tax_superfamily: Optional[str]=None,
                          tax_family: Optional[str]=None,
                          tax_subfamily: Optional[str]=None,
                          tax_genus: Optional[str]=None,
                          tax_species: Optional[str]=None,
                          tax_subspecies: Optional[str]=None,
                          common_name: Optional[str]=None,
                          display_species: Optional[str]=None,) -> HARM_Data_Species:
        params = {x: y for x, y in locals().items() if x.startswith("tax_")}
        params["common_name"] = common_name
        params["display_species"] = display_species
        params = {x: y for x, y in params.items() if y != None}
        if health_check(self.base_url):
            r = requests.get(self.hds_url, 
                            params=params)
            return [HARM_Data_Species(**x) for x in r.json()]
    def get_harm_species(self, species_identifier: UUID):
        if health_check(self.base_url):
            r = requests.get(self.hds_url/species_identifier)
            return HARM_Data_Species(**r.json())
    def delete_harm_species(self, species_identifier: UUID):
        if health_check(self.base_url):
            r = requests.delete(self.hds_url/species_identifier)
    def assign_species_to_record(self, species_identifier: UUID, record_hash: str):
        assign_url = self.hds_url / "assign"
        assign_url.args["species_id"] = species_identifier
        assign_url.args["record_hash"] = record_hash
        if health_check(self.base_url):
            r = requests.post(assign_url)