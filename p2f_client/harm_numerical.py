# Local libraries
from p2f_pydantic.harm_data_numerical import HARM_Float, HARM_Float_Confidence
from p2f_pydantic.harm_data_numerical import HARM_Int, HARM_Int_Confidence
from p2f_pydantic.harm_data_numerical import Insert_HARM_Numerical, Return_HARM_Numerical
from .conn import health_check
# Third Party Libraries
import requests
from furl import furl
# Batteries included libraries
from uuid import UUID
from typing import Optional, List, Union, Literal

Harm_numerical_union = Union[HARM_Int, HARM_Int_Confidence, HARM_Float, HARM_Float_Confidence]

class harm_numerical:
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "harm-numerical/"
        self.hdn_url = self.base_url / self.prefix
        self.harmonized_numerical_records_queue = []
    def add_harm_numerical(self, new_numerical_record: Insert_HARM_Numerical):
        self.harmonized_numerical_records_queue.append(new_numerical_record)
    def upload_harm_numericals(self):
        inserted_numericals = []
        if health_check(self.base_url):
            for nummer in self.harmonized_numerical_records_queue:
                r = requests.post(self.hdn_url, 
                                  data=self.p2fclient.json_serialize_with_auth("new_numeric", nummer.model_dump_json(exclude_unset=True)),
                            headers={"Content-Type": "application/json"})
                inserted_numericals.append(self.identify_numeric_object(r.json(), nummer.model_dump_json(exclude_unset=True)))
            return inserted_numericals
    def upload_harm_numerical(self, new_record: Insert_HARM_Numerical):
        if health_check(self.base_url):
            r = requests.post(self.hdn_url, data=self.p2fclient.json_serialize_with_auth("new_numeric", new_record.model_dump_json(exclude_unset=True)),
                            headers={"Content-Type": "application/json"})
            return self.identify_numeric_object(r.json(), new_record.model_dump(exclude_unset=True))
    def list_harm_numericals(self, 
                             record_hash: Optional[str]=None,
                             numeric_type: Optional[Literal["float_confidence", 
                                                        "float", 
                                                        "int_confidence", 
                                                        "int"]]=None, 
                             data_type: Optional[UUID]=None, 
                             dataset_id: Optional[UUID]=None):
        params = {
            "record_hash": record_hash,
            "numeric_type": numeric_type,
            "data_type": data_type,
            "dataset_id": dataset_id
        }
        params = {x:y for x, y in params.items() if y != None}
        if health_check(self.base_url):
            r = requests.get(self.hdn_url, 
                            params=params, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
            return Return_HARM_Numerical(**r.json())
    def identify_numeric_object(self, 
                                incoming_json, 
                                original: Optional[Insert_HARM_Numerical]=None) -> Harm_numerical_union:
        if original:
            number_type = original["numerical_type"]
        else:
            incoming_value = incoming_json["value"]
            if "." in str(incoming_value):
                number_type = "FLOAT"
            else:
                number_type = "INT"
        if "upper_conf_value" in incoming_json.keys():
            number_type += "_CONFIDENCE"
        match number_type:
            case "INT":
                rv = HARM_Int(**incoming_json)
            case "INT_CONFIDENCE":
                rv = HARM_Int_Confidence(**incoming_json)
            case "FLOAT":
                rv = HARM_Float(**incoming_json)
            case "FLOAT_CONFIDENCE":
                rv = HARM_Float_Confidence(**incoming_json)
        return rv
        


    