# Local libraries
from p2f_pydantic.harm_data_types import HARM_Data_Type
from .conn import health_check
# Third Party Libraries
import requests
from furl import furl
# Batteries included libraries
from uuid import UUID
from typing import Optional, List

class harm_data_type:
    """Class to host the functions of interacting with HARM_Data_Types on
        on the P2F API. 
    """
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "harm-data-types/"
        self.hdt_url = self.base_url / self.prefix
        self.harm_data_types_queue = []
    def upload_data_type(self, new_data_type: HARM_Data_Type) -> HARM_Data_Type:
        """Upload a HARM_Data_Type directly to the API. 

        :param new_data_type: new data type to be uploaded
        :type new_data_type: p2f_pydantic.harm_data_types.HARM_Data_Type
        :return: HARM_Data_Type as processed by the API
        :rtype: p2f_pydantic.harm_data_types.HARM_Data_Type
        """
        if health_check(self.base_url):
            r = requests.post(self.hdt_url, 
                              data=self.p2fclient.jswa("new_harm_data_type", new_data_type.model_dump_json(exclude_unset=True)),
                            headers={"Content-Type": "application/json"})
            return HARM_Data_Type(**r.json())
    def list_data_types(self, 
                        measure: Optional[str]=None,
                        unit_of_measure: Optional[str]=None,
                        method: Optional[str]=None, 
                        dataset_id: Optional[UUID]=None) -> List[HARM_Data_Type]:
        """List HARM_Data_Types as seen on the API

        :param measure: What does the HARM_Data_Type Measure, defaults to None
        :type measure: Optional[str], optional
        :param unit_of_measure: Unit that data type measures, defaults to None
        :type unit_of_measure: Optional[str], optional
        :param method: How is the measurement calculated, defaults to None
        :type method: Optional[str], optional
        :param dataset_id: Filter data types that are available from a dataset_id, defaults to None
        :type dataset_id: Optional[UUID], optional
        :return: List of HARM_Data_Types that were retrieved
        :rtype: List[p2f_pydantic.harm_data_types.HARM_Data_Type]
        """
        params = {"measure": measure,
                  "unit_of_measure": unit_of_measure,
                  "method": method, 
                  "dataset_id": dataset_id}
        params = {x:y for x, y in params.items() if y != None}
        if health_check(self.base_url):
            r = requests.get(self.hdt_url,
                            params=params, 
                            data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})
            return [HARM_Data_Type(**x) for x in r.json()]
    def get_data_type(self, datatype_id: UUID) -> HARM_Data_Type:
        """Get an individual data type by the datatype_id

        :param datatype_id: API datatype_id
        :type datatype_id: UUID
        :return: Retrieved HARM_Data_Type from API
        :rtype: p2f_pydantic.harm_data_types.HARM_Data_Type
        """
        if health_check(self.base_url):
            r = requests.get(self.hdt_url / datatype_id, 
                             data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})
            return HARM_Data_Type(**r.json())
    def delete_data_type(self, datatype_id: UUID):
        """Delete a datatype from the API endpoint. 

        :param datatype_id: The datatype ID that you want to delete
        :type datatype_id: UUID
        """
        if health_check(self.base_url):
            r = requests.delete(self.hdt_url / datatype_id, 
                                data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})