# Local libraries
from p2f_pydantic.datasets import Datasets
from .conn import health_check
# Third Party Libraries
import requests
from furl import furl
# Batteries included libraries
from uuid import UUID
from typing import Optional, List

class datasets:
    """Class to host the functions of interacting with the P2F API, and 
        uploading, retrieving, and deleting Datasets. 
    """
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "datasets/"
        self.dataset_url = self.base_url / self.prefix
        self.data_model = Datasets
    def upload_dataset(self, dataset: Datasets):
        """Upload a dataset directly to the API. 

        :param dataset: Dataset to be uploaded to the API
        :type dataset: p2f_pydantic.datasets.Datasets
        :return: Dataset as ingested by the API
        :rtype: p2f_pydantic.datasets.Datasets
        """
        if health_check(self.base_url):
            r = requests.post(self.dataset_url,
                            data=self.p2fclient.jswa("dataset", dataset.model_dump_json(exclude_unset=True)),
                            headers={"Content-Type": "application/json"})
            return Datasets(**r.json())
    def list_remote_datasets(self, 
                             is_new_p2f: Optional[bool]=None,
                             is_sub_dataset: Optional[bool]=None,
                             doi: Optional[str]=None) -> List[Datasets]:
        """List datasets from the API

        :param is_new_p2f: If the dataset is original to the P2F project (True) or 
            was created by a previous project (False), defaults to None
        :type is_new_p2f: Optional[bool], optional
        :param is_sub_dataset: _description_, defaults to None
        :type is_sub_dataset: Optional[bool], optional
        :param doi: _description_, defaults to None
        :type doi: Optional[str], optional
        :return: _description_
        :rtype: List[Datasets]
        """
        list_url = self.dataset_url
        # data = {}
        if is_new_p2f is not None:
            list_url.args["is_new_p2f"] = is_new_p2f
            # data["is_new_p2f"] = is_new_p2f
        if is_sub_dataset is not None:
            list_url.args["is_sub_dataset"] = is_sub_dataset
            # data["is_sub_dataset"] = is_sub_dataset
        if doi is not None:
            list_url.args["doi"] = doi
            # data["doi"] = doi
        if health_check(self.base_url):
            r = requests.get(list_url, data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})
            # self.datasets = [Datasets(**x) for x in r.json()]
            return [Datasets(**x) for x in r.json()]
    def get_remote_dataset(self, dataset_id: UUID | str):
        """Get a single dataset record by the dataset ID
        
        Parameters
        ----------
        dataset_id : UUID or str
            Dataset ID of a single dataset to retrieve
        """
        get_url = self.dataset_url / str(dataset_id)
        if health_check(self.base_url):
            r = requests.get(get_url, data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})
            return Datasets(**r.json())
    def delete_remote_dataset(self, dataset_id: UUID | str):
        """Delete a single dataset record by the dataset ID
        
        Parameters
        ----------
        dataset_id : UUID or str
            Dataset ID of a single dataset to delete
        """
        delete_url = self.dataset_url / str(dataset_id)
        if health_check(self.base_url):
            r = requests.delete(delete_url, data=self.p2fclient.jswa(),
                            headers={"Content-Type": "application/json"})