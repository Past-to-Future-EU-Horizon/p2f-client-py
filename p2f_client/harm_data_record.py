# Local libraries
from p2f_pydantic.harm_data_record import harm_data_record as Harm_data_record
# Third Party Libraries
import requests
from furl import furl
# Batteries included libraries
from uuid import UUID
from typing import Optional, List

class harm_data_records:
    def __init__(self, base_url):
        self.base_url = furl(base_url)
        self.prefix = "harm-data-records"
        self.hdr_url = self.base_url / self.prefix
        self.harm_data_records = []
    def add_data_record(self, data_record: Harm_data_record):
        self.harm_data_records.append(data_record)
    def upload_data_records(self):
        uploaded_records = []
        for record in self.harm_data_records:
            r = requests.post(self.hdr_url,
                              data=record.model_dump_json(exclude_unset=True))
            record.append(Harm_data_record(**r.json()))
        self.uploaded_records = uploaded_records
    def upload_data_record(self, data_record: Harm_data_record):
        r = requests.post(self.hdr_url,
                          data=data_record.model_dump_json(exclude_unset=True))
        return Harm_data_record(**r.json())
    def list_remote_records(self):
        pass
    def get_remote_record(self):
        pass
    def delete_remote_dataset(self):
        pass