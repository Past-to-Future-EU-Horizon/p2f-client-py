# Local libraries
from p2f_pydantic.harm_data_record import HARM_Data_Record
from .conn import health_check
# Third Party Libraries
import requests
from furl import furl
# Batteries included libraries
from uuid import UUID
from typing import Optional, List
import hashlib
from datetime import datetime
from zoneinfo import ZoneInfo

class harm_data_records:
    """Class for interacting with individual data records/rows from a dataset and the  
        P2F API. """
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "harm-data-records/"
        self.hdr_url = self.base_url / self.prefix
        self.harm_data_records_queue = []
    def upload_data_record(self, data_record: HARM_Data_Record):
        """Upload a HARM_Data_Record directly to the API

        :param data_record: A data record to be directly added to the API
        :type data_record: p2f-pydantic.harm_data_record.HARM_Data_Record
        :return: The object as uploaded to the API
        :rtype: p2f-pydantic.harm_data_record.HARM_Data_Record
        """
        if health_check(self.base_url):
            r = requests.post(self.hdr_url,
                            data=self.p2fclient.json_serialize_with_auth("new_data_record", data_record.model_dump_json(exclude_unset=True)),
                            headers={"Content-Type": "application/json"})
            return HARM_Data_Record(**r.json())
    def list_remote_records(self, 
                            dataset: Optional[str]=None,
                            data_type: Optional[str]=None):
        """List data records on the API. 

        :param dataset: Filter by dataset_id, defaults to None
        :type dataset: Optional[str] representing the dataset_id, optional
        :param data_type: Filter by data_type using a data type id, defaults to None
        :type data_type: Optional[str] representing the data_type_id, optional
        :return: List of HARM_Data_Records found with the query
        :rtype: List[HARM_Data_Record]
        """
        params = {"dataset": dataset,
                  "data_type": data_type}
        params = {x:y for x, y in params.items() if y != None}
        if health_check(self.base_url):
            r = requests.get(self.hdr_url,
                            params=params, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
            return [HARM_Data_Record(**x) for x in r.json()]
    def get_remote_record(self, record_hash: str):
        """Get an individual HARM_Data_Record by record_hash

        :param record_hash: The record hash of the remote dataset
        :type record_hash: str
        :return: HARM_Data_Record
        :rtype: p2f-pydantic.harm_data_record.HARM_Data_Record
        """
        if health_check(self.base_url):
            r = requests.get(self.hdr_url / record_hash, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
            return HARM_Data_Record(**r.json())
    def delete_remote_dataset(self, record_hash: str):
        """Delete a HARM_Data_Record by the record hash from the API

        :param record_hash: record_hash of the HARM_Data_Record on the API
        :type record_hash: str
        """
        if health_check(self.base_url):
            r = requests.delete(self.hdr_url / record_hash, data=self.p2fclient.json_serialize_with_auth(),
                            headers={"Content-Type": "application/json"})
    def calculate_hash(self, dataset_id: str, row_number: int, debugging=False):
        """Utility function for calculating a repeatable hash for the API

        :param dataset_id: dataset_id from the API for the target dataset of the record
        :type dataset_id: str
        :param row_number: Row within the dataset the record represents
        :type row_number: int
        :param debugging: Testing mode that will make all record hashes unique 
            with time, defaults to False
        :type debugging: bool, optional
        :return: A hashed representation of the data record (dataset row)
        :rtype: str
        """
        hasher = hashlib.md5()
        hasher.update(str(dataset_id).encode("utf8"))
        hasher.update(str(row_number).encode("utf8"))
        if debugging == True:
            hasher.update(str(datetime.now(tz=ZoneInfo("UTC")).isoformat(sep="T")).encode("utf8"))
        return str(hasher.hexdigest())