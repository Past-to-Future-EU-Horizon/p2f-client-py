# Local libraries
from p2f_pydantic.keywords import Keywords, TaxonomicDict
from .conn import health_check
# Third Party Libraries
import requests
# Batteries included libraries
from uuid import UUID
from typing import Optional, List
from json import loads

class keywords:
    """Class to interact with HARM Timeslices on the API
    """
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "keywords/"
        self.key_url = self.base_url / self.prefix
        self.data_model = Keywords
        self.taxonomic_data_model = TaxonomicDict
    def add_keyword_to_dataset(self, 
                               new_keyword: Keywords | str,
                               dataset_id: UUID):
        if type(new_keyword) == str:
            new_keyword = Keywords(keyword=new_keyword)
        local_url = self.key_url / "dataset" / dataset_id
        if health_check(self.base_url):
            r = requests.post(local_url,
                              data=new_keyword.model_dump_json(exclude_unset=True),
                              headers=self.p2fclient.base_headers)
    def list_keywords(self, 
                      dataset_id: Optional[UUID]=None, 
                      contains: Optional[str]=None) -> List[Keywords]:
        if health_check(self.base_url):
            local_params = {"dataset_id": dataset_id,
                            "contains": contains}
            local_params = {x:y for x, y in local_params.items() if y is not None}
            r = requests.get(self.key_url,
                             headers=self.p2fclient.base_headers,
                             params=local_params)
            return [Keywords(**x) for x in r.json()]
    def delete_keyword(self, 
                       dataset_id: UUID,
                       keyword: str):
        if health_check(self.base_url):
            local_url = self.key_url / "dataset" / dataset_id
            r = requests.delete(local_url, 
                                headers=self.p2fclient.base_headers,
                                params={"keyword": keyword})
    def list_dictionary(self, 
                        taxonomy: Optional[str]=None,
                        contains: Optional[str]=None) -> List[TaxonomicDict]:
        if health_check(self.base_url):
            local_url = self.key_url / "taxonomies"
            params = {"taxonomy": taxonomy, 
                      "contains": contains}
            params = {x: y for x, y in params if y is not None}
            r = requests.get(local_url,
                             headers=self.p2fclient.base_headers,
                             params=params)
            return loads(r.json())
        
    def assign_taxon_to_dataset(self,
                                taxdict_id: UUID, 
                                dataset_id: UUID):
        if health_check(self.base_url):
            local_url = self.key_url / "dictionary" / taxdict_id
            r = requests.post(url=local_url, 
                              headers=self.p2fclient.base_headers,
                              params={"dataset_id": dataset_id})
    def remove_taxon_from_dataset(self,
                                  taxdict_id: UUID,
                                  dataset_id: UUID):
        if health_check(self.base_url):
            local_url = self.key_url / "dictionary" / taxdict_id
            r = requests.delete(url=local_url,
                                headers=self.p2fclient.base_headers, 
                                params={"dataset_id": dataset_id})
