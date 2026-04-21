# Local libraries
from p2f_pydantic.harm_data_metadata import HARM_Data_Species
from .conn import health_check
# Third Party Libraries
import requests
# Batteries included libraries
from typing import Optional, List
from uuid import UUID

class harm_species:
    """Client library endpoint for interacting with the Harmonized Species data model 
        on the P2F API"""
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "harm-data-species/"
        self.hds_url = self.base_url / self.prefix
        self.harmonized_species_queue = []
    def upload_harm_species(self, new_species: HARM_Data_Species) -> HARM_Data_Species:
        """Upload a HARM_Data_Species directly to the API

        :param new_species: The new species object to be uploaded
        :type new_species: p2f_pydantic.harm_data_metadata.HARM_Data_Species
        :return: The new species object as processed by the API
        :rtype: p2f_pydantic.harm_data_metadata.HARM_Data_Species
        """
        if health_check(self.base_url):
            r = requests.post(self.hds_url, 
                              data=self.p2fclient.jswa("new_species", new_species.model_dump_json(exclude_unset=True)),
                            headers={"Content-Type": "application/json"})
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
                          display_species: Optional[str]=None,) -> List[HARM_Data_Species]:
        """List species that exist on the API based on taxonomy, common name, or the display name.
            Due to writing styles, common name and display name are unreliable search parameters
                at this time. 

        :param tax_*: The taxonomic variable to filter on, defaults to None
        :type tax_*: Optional[str], optional
        :param common_name: Common name of the species, defaults to None
        :type common_name: Optional[str], optional
        :param display_species: Display name of the species, defaults to None
        :type display_species: Optional[str], optional
        :return: A list of species found that match the filters
        :rtype: List[p2f_pydantic.harm_data_metadata.HARM_Data_Species]
        """
        params = {x: y for x, y in locals().items() if x.startswith("tax_")}
        params["common_name"] = common_name
        params["display_species"] = display_species
        params = {x: y for x, y in params.items() if y != None}
        if health_check(self.base_url):
            r = requests.get(self.hds_url, 
                            params=params, data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})
            return [HARM_Data_Species(**x) for x in r.json()]
    def get_harm_species(self, species_identifier: UUID) -> HARM_Data_Species:
        """Get an individual harm species based on the API species id

        :param species_identifier: A species ID from the API
        :type species_identifier: UUID
        :return: The species as retrieved from the API 
        :rtype: p2f_pydantic.harm_data_metadata.HARM_Data_Species
        """
        if health_check(self.base_url):
            r = requests.get(self.hds_url/species_identifier, data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})
            return HARM_Data_Species(**r.json())
    def delete_harm_species(self, species_identifier: UUID):
        """Delete a species from the P2F API

        :param species_identifier: species identifier from the API
        :type species_identifier: UUID
        """
        if health_check(self.base_url):
            r = requests.delete(self.hds_url/species_identifier, data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})
    def assign_species_to_record(self, species_identifier: UUID, record_hash: str):
        """Assign a species to a data record using the record hash. 

        :param species_identifier: species identifier
        :type species_identifier: UUID
        :param record_hash: record hash of the data record
        :type record_hash: str
        """
        assign_url = self.hds_url / "assign"
        assign_url.args["species_id"] = species_identifier
        assign_url.args["record_hash"] = record_hash
        if health_check(self.base_url):
            r = requests.post(assign_url, data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})
    def remove_species_from_record(self, species_identifier: UUID, record_hash: str):
        """Remove a species assigned to a data record using the record hash. 

        :param species_identifier: species identifier
        :type species_identifier: UUID
        :param record_hash: record hash of the data record
        :type record_hash: str
        """
        remove_url = self.hds_url / "assign"
        remove_url.args["species_id"] = species_identifier
        remove_url.args["record_hash"] = record_hash
        if health_check(self.base_url):
            r = requests.post(remove_url, data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})