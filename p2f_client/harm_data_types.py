# Local libraries
from p2f_pydantic.harm_data_types import HARM_Data_Type
# Third Party Libraries
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
        self.data_model = HARM_Data_Type
    def upload_data_type(self, new_data_type: HARM_Data_Type) -> HARM_Data_Type:
        """Upload a HARM_Data_Type directly to the API. 

        :param new_data_type: new data type to be uploaded
        :type new_data_type: p2f_pydantic.harm_data_types.HARM_Data_Type
        :return: HARM_Data_Type as processed by the API
        :rtype: p2f_pydantic.harm_data_types.HARM_Data_Type
        """
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.post(self.hdt_url, 
                                data=new_data_type.model_dump_json(exclude_unset=True))
                return HARM_Data_Type(**r.json())
    def list_data_types(self, 
                        measure: Optional[str]=None,
                        unit_of_measure: Optional[str]=None,
                        method: Optional[str]=None, 
                        dataset_id: Optional[UUID]=None,
                        location_id: Optional[UUID]=None,
                        is_proxy: Optional[bool]=None,
                        active_datatypes: Optional[bool]=None) -> List[HARM_Data_Type]:
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
        if dataset_id is not None:
            dataset_id = str(dataset_id)
        if location_id is not None:
            location_id = str(location_id)
        params = {"measure": measure,
                  "unit_of_measure": unit_of_measure,
                  "method": method, 
                  "dataset_id": dataset_id,
                  "location_id": location_id,
                  "is_proxy": is_proxy,
                  "active_datatypes": active_datatypes}
        params = {x:y for x, y in params.items() if y != None}
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.get(self.hdt_url,
                                params=params)
                return [HARM_Data_Type(**x) for x in r.json()]
    def get_data_type(self, datatype_id: UUID) -> HARM_Data_Type:
        """Get an individual data type by the datatype_id

        :param datatype_id: API datatype_id
        :type datatype_id: UUID
        :return: Retrieved HARM_Data_Type from API
        :rtype: p2f_pydantic.harm_data_types.HARM_Data_Type
        """
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.get(self.hdt_url / str(datatype_id))
                return HARM_Data_Type(**r.json())
    def delete_data_type(self, datatype_id: UUID):
        """Delete a datatype from the API endpoint. 

        :param datatype_id: The datatype ID that you want to delete
        :type datatype_id: UUID
        """
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.delete(self.hdt_url / str(datatype_id))
    def assign_data_type_to_dataset(self, 
                                    datatype_id: UUID, 
                                    dataset_id: UUID):
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                assign_url = self.hdt_url / str(datatype_id) / "assign" / str(dataset_id)
                r = session.post(assign_url)
    def remove_data_type_from_dataset(self,
                                      datatype_id: UUID, 
                                      dataset_id: UUID):
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                remove_url = self.hdt_url / str(datatype_id) / "remove" / str(dataset_id)
                r = session.delete(remove_url)