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
    """Client endpoint for interacting with numerical data types in the P2F API
    """
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "harm-numerical/"
        self.hdn_url = self.base_url / self.prefix
        self.data_model = Insert_HARM_Numerical
    def upload_harm_numerical(self, new_record: Insert_HARM_Numerical):
        """Upload a harm numerical object directly to the API

        :param new_record: _description_
        :type new_record: Insert_HARM_Numerical
        :return: numerical object as processed by the API
        :rtype: object from p2f_pydantic.harm_data_numerical
        """
        if health_check(self.base_url):
            r = requests.post(self.hdn_url, data=self.p2fclient.jswa("new_numeric", new_record.model_dump_json(exclude_unset=True)),
                            headers={"Content-Type": "application/json"})
            return self.identify_numeric_object(r.json(), new_record.model_dump(exclude_unset=True))
    def list_harm_numericals(self, 
                             record_hash: Optional[str]=None,
                             numeric_type: Optional[Literal["float_confidence", 
                                                        "float", 
                                                        "int_confidence", 
                                                        "int"]]=None, 
                             data_type: Optional[UUID]=None, 
                             dataset_id: Optional[UUID]=None) -> Return_HARM_Numerical:
        """Get a list of numerical objects from the P2F API

        :param record_hash: Record hash, defaults to None
        :type record_hash: Optional[str], optional
        :param numeric_type: Integer or Floating point number with or without confidence interval, defaults to None
        :type numeric_type: Optional[Literal[float_confidence, float, int_confidence, int]], optional
        :param data_type: Data type id, defaults to None
        :type data_type: Optional[UUID], optional
        :param dataset_id: dataset_id, defaults to None
        :type dataset_id: Optional[UUID], optional
        :return: Return_HARM_Numerical object
        :rtype: Return_HARM_Numerical
        """
        params = {
            "record_hash": record_hash,
            "numeric_type": numeric_type,
            "data_type": data_type,
            "dataset_id": dataset_id
        }
        params = {x:y for x, y in params.items() if y != None}
        if health_check(self.base_url):
            r = requests.get(self.hdn_url, 
                            params=params, data=self.p2fclient.jswa(),
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
        


    