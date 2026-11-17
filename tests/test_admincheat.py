from os import getenv
import uuid
from random import choice
from p2f_client.p2f_client import P2F_Client
from typing import Literal
from logger_tests import logger

P2F_TEST_ADMIN_EMAIL = getenv("P2F_TEST_ADMIN_EMAIL")
P2F_TEST_ADMIN_TOKEN = getenv("P2F_TEST_ADMIN_TOKEN")
P2F_API_HOSTNAME = getenv("P2F_API_HOSTNAME")
P2F_API_PORT = getenv("P2F_API_PORT")
P2F_API_HTTPS = False


def create_admin_client() -> P2F_Client:
    logger.debug("ADMIN CHEAT: Creating client")
    client = P2F_Client(hostname=P2F_API_HOSTNAME,
                            port=P2F_API_PORT,
                            https=P2F_API_HTTPS,
                            email=P2F_TEST_ADMIN_EMAIL,
                            token=P2F_TEST_ADMIN_TOKEN)
    return client


def get_random_existing_uuid(endpoint: Literal["dataset",
                                               "datatype", 
                                               "location",]) -> uuid.UUID:
    client = create_admin_client()
    logger.debug(f"ADMIN CHEAT: Grabbing a random UUID for {endpoint}")
    match endpoint:
        case "dataset":
            datasets = client.datasets.list_remote_datasets(is_sub_dataset=True)
            datasets = [x.dataset_id for x in datasets]
            rv = choice(datasets)
        case "datatype":
            datatypes = client.harm_data_type.list_data_types()
            datatypes = [x.datatype_id for x in datatypes]
            rv = choice(datatypes)
        case "location":
            locations = client.harm_location.list_harm_locations()
            locations = [x.location_id for x in locations]
            rv = choice(locations)
    logger.debug(f"Sending {rv}")
    return rv