from random import randint, choice
from secrets import token_urlsafe
from datetime import date
from p2f_client.p2f_client import P2F_Client

def insert_datasets(client: P2F_Client):
    new_dataset = client.datasets.data_model(doi=f"11.{token_urlsafe(64)[:5]}/{token_urlsafe(64)[:8]}",
                                             title=f"New parent dataset from {client.auth_email}",
                                             is_sub_dataset=False, 
                                             is_new_p2f=choice([True, False]),
                                             publication_date=date(randint(1900, 2026),
                                                                   randint(1, 12),
                                                                   randint(1, 28)))
    new_dataset = client.datasets.upload_dataset(new_dataset)
    for subdataset in range(randint(1, 6)):
        new_subdataset = client.datasets.data_model(doi=new_dataset.doi,
                                                    title=new_dataset.title,
                                                    is_sub_dataset=True,
                                                    is_new_p2f=new_dataset.is_new_p2f, 
                                                    publication_date=new_dataset.publication_date,
                                                    sub_dataset_name=f"Subdataset {subdataset} from {client.auth_email}")
        client.datasets.upload_dataset(new_subdataset)

def list_datasets(client: P2F_Client):
    dataset_list = client.datasets.list_remote_datasets()
    print(dataset_list)