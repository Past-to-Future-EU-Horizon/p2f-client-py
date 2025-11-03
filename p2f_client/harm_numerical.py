# Local libraries
from p2f_pydantic.harm_data_numerical import insert_harm_numerical as Insert_harm_numerical
from p2f_pydantic.harm_data_numerical import harmonized_float as Harmonized_float
from p2f_pydantic.harm_data_numerical import harmonized_float_confidence as Harmonized_float_confidence
from p2f_pydantic.harm_data_numerical import harmonized_int as Harmonized_int
from p2f_pydantic.harm_data_numerical import harmonized_int_confidence as Harmonized_int_confidence
from p2f_pydantic.harm_data_numerical import return_harm_numerical as Return_harm_numerical
# Third Party Libraries
import requests
from furl import furl
# Batteries included libraries
from uuid import UUID
from typing import Optional, List, Union

Harm_numerical_union = Union[Harmonized_float_confidence, 
                             Harmonized_float,
                             Harmonized_int_confidence,
                             Harmonized_int]

class harm_numerical:
    def __init__(self, base_url):
        self.base_url = furl(base_url)
        self.prefix = "harm-numerical"
        self.hdn_url = self.base_url / self.prefix
        self.harmonized_numerical_records = []
    def add_harm_numerical(self, new_numerical_record: Insert_harm_numerical):
        self.harmonized_numerical_records.append(new_numerical_record)
    def upload_harm_numericals(self):
        inserted_numericals = []
        for nummer in self.harmonized_numerical_records:
            r = requests.post(self.hdn_url,
                              data=nummer.model_dump_json(exclude_unset=True))
    def upload_harm_numerical(self, new_record: Insert_harm_numerical):
        r = requests.post(self.hdn_url,
                          data=new_record)
    def list_harm_numericals(self):
        r = requests.get(self.hdn_url)
        self.harmonized_numerical_records = Return_harm_numerical(**r.json())