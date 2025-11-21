# Local libraries
from p2f_pydantic.harm_data_record import harm_data_record as Harm_data_record
# Third Party Libraries
import requests
from furl import furl
import pytz
# Batteries included libraries
from uuid import UUID
from typing import Optional, List
import hashlib
from datetime import datetime

class harm_data_records:
    def __init__(self, base_url):
        self.base_url = furl(base_url)
        self.prefix = "harm-data-records"
        self.hdr_url = self.base_url / self.prefix
        self.harm_data_records_queue = []
    def add_data_record(self, data_record: Harm_data_record):
        self.harm_data_records_queue.append(data_record)
    def upload_data_records(self):
        uploaded_records = []
        for record in self.harm_data_records_queue:
            r = requests.post(self.hdr_url,
                              data=record.model_dump_json(exclude_unset=True))
            record.append(Harm_data_record(**r.json()))
        self.uploaded_records = uploaded_records
        return uploaded_records
    def upload_data_record(self, data_record: Harm_data_record):
        r = requests.post(self.hdr_url,
                          data=data_record.model_dump_json(exclude_unset=True))
        return Harm_data_record(**r.json())
    def list_remote_records(self, 
                            dataset: Optional[str]=None,
                            data_type: Optional[str]=None):
        params = {"dataset": dataset,
                  "data_type": data_type}
        params = {x:y for x, y in params.items() if y != None}
        r = requests.get(self.hdr_url,
                         data=params)
        return [Harm_data_record(**x) for x in r.json()]
    def get_remote_record(self, record_hash: str):
        r = requests.get(self.hdr_url / record_hash)
        return Harm_data_record(**r.json())
    def delete_remote_dataset(self, record_hash: str):
        r = requests.delete(self.hdr_url / record_hash)
    def calculate_hash(self, dataset_id, row_number, debugging=False):
        hasher = hashlib.md5()
        hasher.update(str(dataset_id).encode("utf8"))
        hasher.update(str(row_number).encode("utf8"))
        if debugging == True:
            hasher.update(str(datetime.now(tz=pytz.UTC).isoformat(sep="T")).encode("utf8"))
        return str(hasher.hexdigest())