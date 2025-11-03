# Local libraries
from p2f_pydantic.harm_data_types import harm_data_type as Harm_data_type
# Third Party Libraries
import requests
from furl import furl
# Batteries included libraries
from uuid import UUID
from typing import Optional, List

class harm_data_type:
    def __init__(self, base_url):
        self.base_url = furl(base_url)
        self.prefix = "harm-data-types"
        self.hdt_url = self.base_url / self.prefix
        self.harm_data_types = []
    def add_harm_data_type(self, new_data_type: Harm_data_type):
        self.harm_data_types.append(new_data_type)
    def upload_data_types(self):
        for datatype in self.harm_data_types:
            r = requests.post(self.hdt_url,
                              data=datatype.model_dump_json(exclude_unset=True))
    def upload_data_type(self, new_data_type: Harm_data_type):
        r = requests.post(self.hdt_url,
                          data=new_data_type.model_dump_json(exclude_unset=True))
        return Harm_data_type(**r.json())
    def list_data_types(self):
        r = requests.get(self.hdt_url)
        self.harm_data_types = [Harm_data_type(**x) for x in r.json()]
    def get_data_type(self):
        pass
    def delete_data_type(self):
        pass