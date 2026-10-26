# Local libraries
from p2f_pydantic.harm_data_numerical import HARM_Float, HARM_Float_Confidence
from p2f_pydantic.harm_data_numerical import HARM_Int, HARM_Int_Confidence
from p2f_pydantic.harm_data_numerical import Insert_HARM_Numerical, Return_HARM_Numerical
from p2f_pydantic.harm_data_numerical import Numerical_Table_Statistics
from .conn import health_check
from .conn import ACCEPT_DICT, ACCEPT_LIST
# Third Party Libraries
import requests
from furl import furl
import pandas as pd
# Batteries included libraries
from uuid import UUID
from io import StringIO, BytesIO
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
            r = requests.post(self.hdn_url, data=new_record.model_dump_json(exclude_unset=True),
                            headers=self.p2fclient.base_headers)
            return self.identify_numeric_object(r.json(), new_record.model_dump(exclude_unset=True))
    def list_harm_numericals(self, 
                             record_hash: Optional[str]=None,
                             numeric_type: Optional[Literal["float_confidence", 
                                                        "float", 
                                                        "int_confidence", 
                                                        "int"]]=None, 
                             datatype_id: Optional[UUID]=None, 
                             dataset_id: Optional[UUID]=None,
                             request_as: Optional[Literal[ACCEPT_LIST]] = "pandas") -> Return_HARM_Numerical:
        if numeric_type == None:
            remote_stats = self.get_numeric_statistics(dataset_id=dataset_id, datatype_id=datatype_id)
            request_tables = [x.replace("count_", "") for x,y  in remote_stats.model_dump(exclude_unset=True, exclude={"count_total"}).items() if y > 0]
        else:
            request_tables = [numeric_type]
        collected_results = {}
        for numtype in request_tables:
            params = {
                "record_hash": record_hash,
                "numeric_type": numtype,
                "datatype_id": datatype_id,
                "dataset_id": dataset_id
            }
            params = {x:y for x, y in params.items() if y != None}
            headers = self.p2fclient.base_headers
            headers["Accept"] = ACCEPT_DICT[request_as] # This can be a line w/o if/else or match/case, we don't care if the json path is taken and gets set again to application/json
            if health_check(self.base_url):
                r = requests.get(self.hdn_url, 
                                params=params,
                                headers=headers)
                if r.ok:
                    collected_results[numtype] = r.content
        match request_as:
            case "json":
                dictionary_transform = {f"data_harmonized_{x}": y for x, y in collected_results}
                return Return_HARM_Numerical(**dictionary_transform)
            case "csv":
                file = {x: StringIO(y) for x, y in collected_results.items()}
                return file
            case "parquet":
                file = {x: BytesIO(y) for x, y in collected_results.items()}
                return file
            case "pandas":
                dfs = {x: pd.read_parquet(BytesIO(y)) for x, y in collected_results.items()}
                return dfs
                        
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
    def get_numeric_statistics(self,
                               datatype_id: Optional[UUID]=None, 
                               dataset_id: Optional[UUID]=None,) -> Numerical_Table_Statistics:
        params = {"datatype_id": datatype_id,
                  "dataset_id": dataset_id}
        params = {x: y for x, y in params.items() if y is not None}
        headers = self.p2fclient.base_headers
        statistics_url = self.hdn_url / "statistics"
        if health_check(self.base_url):
            r = requests.get(statistics_url,
                             headers=headers,
                             params=params)
            if r.ok:
                return Numerical_Table_Statistics(**r.json())