from p2f_client.p2f_client import P2F_Client
from os import getenv
from time import sleep

P2F_API_HOSTNAME = getenv("P2F_API_HOSTNAME")
P2F_API_PORT = getenv("P2F_API_PORT")
P2F_API_HTTPS = False
P2F_TEST_EMAIL = getenv("P2F_TEST_EMAIL")
P2F_TEST_TOKEN = getenv("P2F_TEST_TOKEN")

print("Client create")
client = P2F_Client(hostname=P2F_API_HOSTNAME,
                    port=P2F_API_PORT,
                    https=P2F_API_HTTPS,
                    email=P2F_TEST_EMAIL,
                    token=P2F_TEST_TOKEN)


print("Final sleep")
sleep(10)