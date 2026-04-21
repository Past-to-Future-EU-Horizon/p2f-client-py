# Local libraries
from p2f_pydantic.harm_data_metadata import HARM_Bounding_Box, HARM_Location
from .conn import health_check
# Third Party Libraries
import requests
from furl import furl
# Batteries included libraries
from uuid import UUID
from typing import Optional, List, Union

class harm_location:
    """Class for interacting with locations on the P2F API. 
    """   
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "harm-data-locations/"
        self.hdl_url = self.base_url / self.prefix
        self.harmonized_location_queue = []
    def upload_harm_location(self, new_location: HARM_Location) -> HARM_Location:
        """Upload a location to the P2F API

        :param new_location: Location to be uploaded to the API
        :type new_location: p2f_pydantic.harm_data_metadata.HARM_Location
        :return: The new location as processed by the API 
        :rtype: p2f_pydantic.harm_data_metadata.HARM_Location
        """
        if health_check(self.base_url):
            r = requests.post(self.hdl_url, 
                              data=self.p2fclient.jswa("new_location", new_location.model_dump_json(exclude_unset=True)),
                            headers={"Content-Type": "application/json"})
            return HARM_Location(**r.json())
    def list_harm_locations(self,
                            bounding_box: Optional[HARM_Bounding_Box]=None,
                            location_name: Optional[str]=None, 
                            location_code: Optional[str]=None, 
                            minimum_elevation: Optional[float]=None,
                            maximum_elevation: Optional[float]=None,
                            min_location_age: Optional[float]=None,
                            max_location_age: Optional[float]=None, 
                            dataset_id: Optional[UUID]=None):
        """A list of locations based on the filters provided. 

        :param bounding_box: Bounding box with N, E, S, W defined in WGS84 Decimal Degrees, defaults to None
        :type bounding_box: Optional[p2f_pydantic.harm_data_metadata.HARM_Bounding_Box], optional
        :param location_name: Name of the location, defaults to None
        :type location_name: Optional[str], optional
        :param location_code: Location code, defaults to None
        :type location_code: Optional[str], optional
        :param minimum_elevation: A minimum elevation in meters above sea level (negative for under sea level/depth), defaults to None
        :type minimum_elevation: Optional[float], optional
        :param maximum_elevation: A maximum elevation in meters above sea level (negative for under sea level/depth), defaults to None
        :type maximum_elevation: Optional[float], optional
        :param dataset_id: Associated dataset ID of the location, defaults to None
        :type dataset_id: Optional[UUID], optional
        :return: List of HARM Locations 
        :rtype: p2f_pydantic.harm_data_metadata.HARM_Location
        """
        params = {
            "bounding_box": bounding_box,
            "location_name": location_name,
            "location_code": location_code, 
            "minimum_elevation": minimum_elevation,
            "maximum_elevation": maximum_elevation,
            "min_location_age": min_location_age,
            "max_location_age": max_location_age,
            "dataset_id": dataset_id
            }
        params = {x: y for x, y in params.items() if y != None}
        if health_check(self.base_url):
            r = requests.get(self.hdl_url,
                            params=params, data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})
            return [HARM_Location(**x) for x in r.json()]
    def get_harm_location(self, location_identifier: UUID) -> HARM_Location:
        """Retrieve an individual HARM Location by its location identifier

        :param location_identifier: Location identifier from the API
        :type location_identifier: UUID
        :return: HARM Location from the API
        :rtype: p2f_pydantic.harm_data_metadata.HARM_Location
        """
        if health_check(self.base_url):
            r = requests.get(self.hdl_url/str(location_identifier), data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})
            return HARM_Location(**r.json())
    def delete_harm_location(self, location_identifier: UUID):
        """Delete a location from the API

        :param location_identifier: location identifier from the API
        :type location_identifier: UUID
        """
        if health_check(self.base_url):
            r = requests.delete(self.hdl_url/str(location_identifier), data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})
    def assign_location_to_record(self, location_identifier: UUID, record_hash: str):
        """Assign a location to a record hash

        :param location_identifier: location identifier from the API
        :type location_identifier: UUID
        :param record_hash: Record hash
        :type record_hash: str
        """
        # params = {"location_identifier": str(location_identifier),
        #           "record_hash": record_hash}
        assign_url = self.hdl_url / "assign"
        assign_url.args["location_identifier"] = str(location_identifier)
        assign_url.args["record_hash"] = record_hash
        if health_check(self.base_url):
            r = requests.post(assign_url, data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})
    def remove_location_from_record(self, location_identifier: UUID, record_hash: str):
        """Remove a location assigned to a record hash

        :param location_identifier: location identifier from the API
        :type location_identifier: UUID
        :param record_hash: Record hash
        :type record_hash: str
        """
        # params = {"location_identifier": str(location_identifier),
        #           "record_hash": record_hash}
        remove_url = self.hdl_url / "remove"
        remove_url.args["location_identifier"] = str(location_identifier)
        remove_url.args["record_hash"] = record_hash
        if health_check(self.base_url):
            r = requests.post(remove_url, data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})