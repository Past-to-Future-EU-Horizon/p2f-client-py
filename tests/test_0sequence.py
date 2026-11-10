from p2f_client.p2f_client import P2F_Client
from os import getenv
from time import sleep
from logger_tests import logger
from report_result import add_report, dump_reports
## Sequence
from test_dataset import insert_datasets, list_datasets

P2F_API_HOSTNAME = getenv("P2F_API_HOSTNAME")
P2F_API_PORT = getenv("P2F_API_PORT")
P2F_API_HTTPS = False
P2F_TEST_EMAIL = getenv("P2F_TEST_EMAIL")
P2F_TEST_TOKEN = getenv("P2F_TEST_TOKEN")


logger.debug("CLIENT CREATE")
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
    add_report(test_name="CREATE CLIENT", output_text=e, status_code=999)

if client_continue:
    insert_datasets(client=client)
    list_datasets(client=client)

logger.debug("DUMP REPORTS")
dump_reports()
logger.debug("FINAL SLEEP")
sleep(10)