# Local libraries
from p2f_pydantic.keywords import Keywords, TaxonomicDict
from .conn import eval_non_ok_return
# Third Party Libraries
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
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.post(local_url,
                                data=new_keyword.model_dump_json(exclude_unset=True))
    def list_keywords(self, 
                      dataset_id: Optional[UUID]=None, 
                      contains: Optional[str]=None) -> List[Keywords]:
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                local_params = {"dataset_id": dataset_id,
                                "contains": contains}
                local_params = {x:y for x, y in local_params.items() if y is not None}
                r = session.get(self.key_url,
                                params=local_params)
                if r.ok:
                    return [Keywords(**x) for x in r.json()]
                else: 
                    eval_non_ok_return(r.status_code)
    def delete_keyword(self, 
                       dataset_id: UUID,
                       keyword: str):
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                local_url = self.key_url / "dataset" / dataset_id
                r = session.delete(local_url,
                                    params={"keyword": keyword})
    def list_dictionary(self, 
                        taxonomy: Optional[str]=None,
                        contains: Optional[str]=None) -> List[TaxonomicDict]:
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                local_url = self.key_url / "taxonomies"
                params = {"taxonomy": taxonomy, 
                        "contains": contains}
                params = {x: y for x, y in params if y is not None}
                r = session.get(local_url,
                                params=params)
                return loads(r.json())
        
    def assign_taxon_to_dataset(self,
                                taxdict_id: UUID, 
                                dataset_id: UUID):
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                local_url = self.key_url / "dictionary" / taxdict_id
                r = session.post(url=local_url,
                                params={"dataset_id": dataset_id})
    def remove_taxon_from_dataset(self,
                                  taxdict_id: UUID,
                                  dataset_id: UUID):
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                local_url = self.key_url / "dictionary" / taxdict_id
                r = session.delete(url=local_url, 
                                    params={"dataset_id": dataset_id})
