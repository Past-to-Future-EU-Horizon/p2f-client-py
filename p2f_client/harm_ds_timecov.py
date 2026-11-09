# Local libraries
from p2f_pydantic.harm_ds_time import HARM_DS_TimeCoverage
# Third Party Libraries
# Batteries included libraries
from uuid import UUID
from typing import Optional, List

class harm_ds_timecoverage:
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "time-coverage/"
        self.tc_url = self.base_url / self.prefix
        self.data_model = HARM_DS_TimeCoverage
    def upload_dataset_timecoverage(self, new_time_coverage: HARM_DS_TimeCoverage) -> HARM_DS_TimeCoverage:
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.post(self.hdt_url, 
                                data=new_time_coverage.model_dump_json(exclude_unset=True))
                return HARM_DS_TimeCoverage(**r.json())
    def get_dataset_timecoverage(self, dataset_id: UUID) -> HARM_DS_TimeCoverage:
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.get(self.hdt_url / str(dataset_id))
                return HARM_DS_TimeCoverage(**r.json())
    def delete_dataset_timecoverage(self, dataset_id: UUID):
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.delete(self.hdt_url / str(dataset_id))