# Local libraries
from p2f_pydantic.datasets import Datasets
# Third Party Libraries
import requests
from furl import furl
# Batteries included libraries
from uuid import UUID
from typing import Optional, List

class datasets:
    def __init__(self, base_url):
        self.base_url = furl(base_url)
        self.prefix = "datasets"
        self.dataset_url = self.base_url / self.prefix
        self.upload_queue = []
    def add_dataset(self, dataset: Datasets):
        self.upload_queue.append(dataset)
    def upload_datasets(self):
        uploaded_datasets = []
        for dataset in self.upload_queue:
            r = requests.post(self.dataset_url,
                              data=dataset.model_dump_json(exclude_unset=True))
            uploaded_datasets.append(Datasets(**r.json()))
        # self.uploaded_datasets = uploaded_datasets
        return uploaded_datasets
    def upload_dataset(self, dataset: Datasets):
        r = requests.post(self.dataset_url,
                          data=dataset.model_dump_json(exclude_unset=True))
        return Datasets(**r.json())
    def list_remote_datasets(self, 
                             is_new_p2f: Optional[bool]=None,
                             is_sub_dataset: Optional[bool]=None,
                             doi: Optional[str]=None) -> List[Datasets]:
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
        r = requests.get(list_url)
        # self.datasets = [Datasets(**x) for x in r.json()]
        return [Datasets(**x) for x in r.json()]
    def get_remote_dataset(self, dataset_id):
        get_url = self.dataset_url / str(dataset_id)
        r = requests.get(get_url)
        return Datasets(**r.json())
    def delete_remote_dataset(self, dataset_id):
        delete_url = self.dataset_url / str(dataset_id)
        r = requests.delete(delete_url)