from random import randint, choice
from secrets import token_urlsafe
from datetime import date
from p2f_client.p2f_client import P2F_Client
from logger_tests import logger
from report_result import add_report

def insert_datasets(client: P2F_Client):
    logger.debug("Running Insert Dataset")
    new_dataset = client.datasets.data_model(doi=f"11.{token_urlsafe(64)[:5]}/{token_urlsafe(64)[:8]}",
                                             title=f"New parent dataset from {client.auth_email}",
                                             is_sub_dataset=False, 
                                             is_new_p2f=choice([True, False]),
                                             publication_date=date(randint(1900, 2026),
                                                                   randint(1, 12),
                                                                   randint(1, 28)))
    logger.debug("Inserting parent dataset")
    try:
        new_dataset = client.datasets.upload_dataset(new_dataset)
        add_report(test_name="PARENT DATASET INSERT", output_text=new_dataset.model_dump_json(exclude_unset=True), status_code=100)
    except Exception as e:
        add_report(test_name="PARENT DATASET INSERT", output_text=e, status_code=999)

    logger.debug("Parent dataset inserted")
    for subdataset in range(randint(1, 6)):
        logger.debug(f"Creating subdataset {subdataset}")
        new_subdataset = client.datasets.data_model(doi=new_dataset.doi,
                                                    title=new_dataset.title,
                                                    is_sub_dataset=True,
                                                    is_new_p2f=new_dataset.is_new_p2f, 
                                                    publication_date=new_dataset.publication_date,
                                                    sub_dataset_name=f"Subdataset {subdataset} from {client.auth_email}")
        logger.debug(f"Inserting subdataset {subdataset}")
        try:
            new_subdataset = client.datasets.upload_dataset(new_subdataset)
            add_report(test_name="SUBDATASET INSERT", output_text=new_subdataset.model_dump_json(exclude_unset=True), status_code=100)
        except Exception as e:
            add_report(test_name="SUBDATASET INSERT", output_text=e, status_code=999)
        logger.debug(f"Subdataset {subdataset} uploaded")

def list_datasets(client: P2F_Client):
    try:
        dataset_list = client.datasets.list_remote_datasets()
        logger.debug(dataset_list)
        add_report(test_name="LIST DATASETS", output_text=f"Total datasets = {len(dataset_list)}", status_code=100)
    except Exception as e:
        add_report(test_name="LIST DATASETS", output_text=e, status_code=999)