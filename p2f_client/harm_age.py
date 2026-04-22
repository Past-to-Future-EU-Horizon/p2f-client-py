# local libraries
from p2f_pydantic.harm_age import HARM_Data_Age
from .conn import health_check
# Third part libraries
import requests
from furl import furl
# Batteries included libraries
from uuid import UUID
from typing import List, Optional

class harm_age:
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "harm-data-age/"
        self.hda_url = self.base_url / self.prefix
        self.data_model = HARM_Data_Age
    def upload_harm_age(self, new_harm_age: HARM_Data_Age) -> HARM_Data_Age:
        """Upload a new HARM Data Age to the API directly. 

        :param new_harm_age: new Data Age object
        :type new_harm_age: p2f_pydantic.harm_age.HARM_Data_Age
        :return: new Harm Data Age object as processed by API
        :rtype: p2f_pydantic.harm_age.HARM_Data_Age
        """
        if health_check(self.base_url):
            r = requests.post(self.hda_url, 
                         data=self.p2fclient.jswa("new_harm_age", new_harm_age.model_dump_json(exclude_unset=True)), 
                         headers={"Content-Type": "application/json"})
            if r.ok:
                return HARM_Data_Age(**r.json())
    def list_harm_ages(self) -> List[HARM_Data_Age]:
        if health_check(self.base_url):
            r = requests.get(self.hda_url, 
                             data=self.p2fclient.jswa(), 
                             headers={"Content-Type": "application/json"})
            if r.ok:
                return [HARM_Data_Age(**x) for x in r.json()]
    def get_harm_age(self, ) -> HARM_Data_Age:
        pass
    def delete_harm_age(self, ) -> HARM_Data_Age:
        pass