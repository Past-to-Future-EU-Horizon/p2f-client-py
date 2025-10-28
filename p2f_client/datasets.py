# Local libraries
from p2f_pydantic.datasets import Datasets
# Third Party Libraries
import requests
# Batteries included libraries

class datasets:
    def __init__(self, base_url):
        self.base_url = base_url
        self.prefix = "datasets"
        self.dataset_url = self.base_url / self.prefix
    def list_datasets(self):
        list_url_endpoint = f"{self.host_url}/{self.prefix}"
        r = requests.get(list_url_endpoint)
        return r.json
    def get_dataset(self):
        get_url_endpoint = f"{self.host_url}/{self.prefix}"
        r = requests.get(get_url_endpoint)
        return r.json
    def create_dataset(self, new_dataset: Datasets):
        create_url_endpoint = f"{self.host_url}/{self.prefix}"
        r = requests.post(create_url_endpoint,
                          json=new_dataset)
    def update_dataset(self, update_dataset: Datasets):
        update_url_endpoint = f"{self.host_url}/{self.prefix}"
        r = requests.put(update_url_endpoint,
                          json=update_dataset)
    def delete_dataset(self, delete_dataset: int | Datasets):
        delete_url_endpoint = f"{self.host_url}/{self.prefix}"
        r = requests.delete(delete_url_endpoint,
                          json=delete_dataset)