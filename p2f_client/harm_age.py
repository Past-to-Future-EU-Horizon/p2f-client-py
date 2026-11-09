# local libraries
from p2f_pydantic.harm_age import HARM_Rec_Age
# Third part libraries
# Batteries included libraries
from uuid import UUID
from typing import List, Optional

class harm_age:
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "harm-data-age/"
        self.hda_url = self.base_url / self.prefix
        self.data_model = HARM_Rec_Age
    def upload_harm_age(self, new_harm_age: HARM_Rec_Age) -> HARM_Rec_Age:
        """Upload a new HARM Data Age to the API directly. 

        :param new_harm_age: new Data Age object
        :type new_harm_age: p2f_pydantic.harm_age.HARM_Rec_Age
        :return: new Harm Data Age object as processed by API
        :rtype: p2f_pydantic.harm_age.HARM_Rec_Age
        """
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.post(self.hda_url, 
                                 data=new_harm_age.model_dump_json(exclude_unset=True))
                if r.ok:
                    return HARM_Rec_Age(**r.json())
    def list_harm_ages(self, 
                       older_year: Optional[int] = None, 
                       recent_year: Optional[int] = None,
                       dataset_id: Optional[UUID] = None,) -> List[HARM_Rec_Age]:
        if dataset_id is not None: 
            dataset_id = str(dataset_id)
        params = {
            "recent_year_search": recent_year,
            "older_year_search": older_year,
            "dataset_id": dataset_id
        }
        params = {x: y for x, y in params if y is not None}
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.get(self.hda_url,
                                params=params)
                if r.ok:
                    return [HARM_Rec_Age(**x) for x in r.json()]
    def get_harm_age(self, record_hash: str) -> HARM_Rec_Age:
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                get_record_url = self.hda_url / record_hash
                r = session.get(get_record_url)
    def delete_harm_age(self, record_hash: str) -> HARM_Rec_Age:
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                delete_record_url = self.hda_url / record_hash
                r = session.delete(delete_record_url)