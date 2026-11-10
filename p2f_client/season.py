# Local libraries
from p2f_pydantic.seasonality import Season
from .conn import eval_non_ok_return
# Third Party Libraries
# Batteries included libraries
from uuid import UUID
from typing import Optional, List
from json import loads

class season:
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "season/"
        self.season_url = self.base_url / self.prefix
        self.data_model = Season
    def add_season(self, 
                   record_hash: str, 
                   new_season: Season):
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                local_url = self.season_url / record_hash
                r = session.post(local_url, 
                                data=new_season.model_dump_json(exclude_unset=True))
                if r.ok:
                    return Season(**r.json())
                else: 
                    eval_non_ok_return(r.status_code)
    def get_season(self, 
                   record_hash: str) -> Season:
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                local_url = self.season_url / record_hash
                r = session.get(local_url)
                if r.ok:
                    return Season(**r.json())
                else: 
                    eval_non_ok_return(r.status_code)
    def delete_season(self, 
                   record_hash: str):
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                local_url = self.season_url / record_hash
                r = session.delete(local_url)