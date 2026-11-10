# Local libraries
from p2f_pydantic.seasonality import Seasonality_DS
from .conn import eval_non_ok_return
# Third Party Libraries
# Batteries included libraries
from uuid import UUID
from typing import Optional, List
from json import loads

class seasonality:
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "seasonality/"
        self.seasonality_url = self.base_url / self.prefix
        self.data_model = Seasonality_DS
    def add_seasonality(self, 
                   dataset_id: UUID, 
                   new_seasonality: Seasonality_DS):
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                local_url = self.seasonality_url / dataset_id
                r = session.post(local_url, 
                                data=new_seasonality.model_dump_json(exclude_unset=True))
                if r.ok:
                    return Seasonality_DS(**r.json())
                else: 
                    eval_non_ok_return(r.status_code)
    def get_seasonality(self, 
                   dataset_id: UUID) -> Seasonality_DS:
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                local_url = self.seasonality_url / dataset_id
                r = session.get(local_url)
                if r.ok:
                    return Seasonality_DS(**r.json())
                else: 
                    eval_non_ok_return(r.status_code)
    def delete_season(self, 
                      dataset_id: UUID):
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                local_url = self.seasonality_url / dataset_id
                r = session.delete(local_url)