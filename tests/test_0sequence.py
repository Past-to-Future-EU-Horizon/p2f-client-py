from p2f_client.p2f_client import P2F_Client
from os import getenv
from time import sleep
from logger_tests import logger
from report_result import add_report, dump_reports
## Sequence
from test_dataset import insert_datasets, list_datasets
from test_datatypes import insert_datatype, list_datatypes
from test_locations import insert_location, list_locations
from test_numeric import create_dataset

P2F_API_HOSTNAME = getenv("P2F_API_HOSTNAME")
P2F_API_PORT = getenv("P2F_API_PORT")
P2F_API_HTTPS = False
P2F_TEST_EMAIL = getenv("P2F_TEST_EMAIL")
P2F_TEST_TOKEN = getenv("P2F_TEST_TOKEN")


logger.debug("SEQUENCE: CLIENT CREATE")
client_continue = False
try:
    client = P2F_Client(hostname=P2F_API_HOSTNAME,
                        port=P2F_API_PORT,
                        https=P2F_API_HTTPS,
                        email=P2F_TEST_EMAIL,
                        token=P2F_TEST_TOKEN)
    add_report(test_name="CREATE CLIENT", output_text="Success", status_code=100)
    client_continue = True
except Exception as e:
    logger.debug("SEQUENCE: Client failed to create")
    add_report(test_name="CREATE CLIENT", output_text=e, status_code=999)

if client_continue:
    logger.debug("SEQUENCE: Client continue is True, starting insert datasets test")
    insert_datasets(client=client)
    logger.debug("SEQUENCE: List datasets")
    list_datasets(client=client)
    logger.debug("SEQUENCE: Insert data types")
    for i in range(10):
        insert_datatype(client=client)
    logger.debug("SEQUENCE: List data types")
    list_datatypes(client=client)
    logger.debug("SEQUENCE: Insert locations")
    for i in range(10):
        insert_location(client=client)
    logger.debug("SEQUENCE: List locations")
    list_locations(client=client)
    logger.debug("SEQUENCE: Create dataset (numeric)")
    create_dataset(client=client)

sleep(5)
logger.debug("SEQUENCE: DUMP REPORTS")
dump_reports()
logger.debug("SEQUENCE: FINAL SLEEP")
sleep(10)