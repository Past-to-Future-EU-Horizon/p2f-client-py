# Local libraries
from p2f_pydantic.harm_data_metadata import harm_location as Harm_location
from p2f_pydantic.harm_data_metadata import harm_bounding_box as Harm_bounding_box
# Third Party Libraries
import requests
from furl import furl
# Batteries included libraries
from uuid import UUID
from typing import Optional, List, Union

class harm_location:
    def __init__(self, base_url):
        self.base_url = base_url
        self.prefix = "harm-data-locations"
        self.hdl_url = self.base_url / self.prefix
        self.harmonized_location_queue = []
    def add_harm_location(self, new_location: Harm_location):
        self.harmonized_location_queue.append(new_location)
    def upload_harm_locations(self):
        inserted_locations = []
        for location in self.harmonized_location_queue:
            r = requests.post(self.hdl_url, 
                              data=location.model_dump_json(exclude_unset=True))
            inserted_locations.append(Harm_location(**r.json()))
        return inserted_locations
    def upload_harm_location(self, new_location: Harm_location):
        r = requests.post(self.hdl_url,
                          data=new_location.model_dump_json(exclude_unset=True))
        return Harm_location(**r.json())
    def list_harm_locations(self,
                            bounding_box: Optional[Harm_bounding_box]=None,
                            location_name: Optional[str]=None, 
                            location_code: Optional[str]=None, 
                            minimum_elevation: Optional[float]=None,
                            maximum_elevation: Optional[float]=None,
                            min_location_age: Optional[float]=None,
                            max_location_age: Optional[float]=None, 
                            dataset_id: Optional[UUID]=None):
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
        r = requests.get(self.hdl_url,
                         params=params)
        return [Harm_location(**x) for x in r.json()]
    def get_harm_location(self, location_identifier: UUID):
        r = requests.get(self.hdl_url/str(location_identifier))
        return Harm_location(**r.json())
    def delete_harm_location(self, location_identifier: UUID):
        r = requests.delete(self.hdl_url/str(location_identifier))
    def assign_location_to_record(self, location_identifier: UUID, record_hash: str):
        # params = {"location_identifier": str(location_identifier),
        #           "record_hash": record_hash}
        assign_url = self.hdl_url / "assign"
        assign_url.args["location_identifier"] = str(location_identifier)
        assign_url.args["record_hash"] = record_hash
        r = requests.post(assign_url)