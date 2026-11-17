from uuid import uuid4
from pprint import pprint
from copy import deepcopy
from typing import List, Dict
from random import randint, choice
from os import mkdir, getcwd
from datetime import datetime
import socket
from time import sleep
import docker

test_run_id = uuid4()
shtrid = f"{str(hex(test_run_id.fields[-1]))[2:]}"

print(shtrid)

client = docker.from_env()

print("Gathering configuration from running Docker P2F-API container")

# Get the latest API Container 
p2f_api_container = client.containers.list()
api_containers = [x for x in client.containers.list() if x.name.startswith("p2f_api_")]
api_containers = {x.attrs["Created"]: x for x in api_containers}
api_containers = {datetime.strptime(f"{x.split('.')[0]}Z", "%Y-%m-%dT%H:%M:%SZ"): y for x, y in api_containers.items()}
api_container = api_containers[max(list(api_containers.keys()))]

# Get the container environment
api_config = api_container.attrs["Config"]["Env"]
# In case there is another = elsewhere in the environment variable (I'm not sure that's possible) we grab the first portion, then slice off the rest
api_config = {x.split("=")[0]: x.replace(f'{x.split("=")[0]}=', '') for x in api_config}

# Get the network of the running API container
api_network_config = api_container.attrs["NetworkSettings"]
api_network = [x for x in api_network_config["Networks"].keys() if x.startswith("p2f_network_test")][0]

# Get the DNS name of the api container within the network, select the first value
api_dns_name = api_network_config["Networks"][api_network]["DNSNames"][0]

def get_logs_docker(container=api_container):
    logs = container.logs()
    logs = logs.decode("utf8")
    return logs

def extract_token(logs, email):
    next_line_password = False
    current_email = "" 
    password = None
    for line in logs.split("\n"):
        if next_line_password:
            password = line
            next_line_password = False
        if "Your token for the P2F Portal is below" in line and current_email == email:
            next_line_password = True
        if "To: " in line:
            current_email = line[4:]
            # print(current_email == email)
    return password

api_container_logs = get_logs_docker(container=api_container)
admin_token = extract_token(logs=api_container_logs, email=api_config["P2F_ADMIN_EMAIL_ADDRESS"])


base_environment = {
    "P2F_API_HOSTNAME": api_dns_name,
    "P2F_API_PORT": 8084,
    "P2F_API_HTTPS": False,
    "PG_USER": api_config["PG_USER"],
    "PG_PASS": api_config["PG_PASS"],
    "PG_HOST": api_config["PG_HOST"],
    "PG_PORT": api_config["PG_PORT"],
    "PG_DB": api_config["PG_DB"],
    "P2F_TEST_ADMIN_EMAIL": api_config["P2F_ADMIN_EMAIL_ADDRESS"],
    "P2F_TEST_ADMIN_TOKEN": admin_token
}

# Set the PORTAL environment
as_portal_environment = deepcopy(base_environment)
as_portal_environment["P2F_TEST_EMAIL"] = api_config["P2F_PORTAL_EMAIL_ADDRESS"]
as_portal_environment["P2F_TEST_TOKEN"] = api_config["P2F_PORTAL_TOKEN"]

# Set the ADMIN environment
as_admin_environment = deepcopy(base_environment)
as_admin_environment["P2F_TEST_EMAIL"] = api_config["P2F_ADMIN_EMAIL_ADDRESS"]
as_admin_environment["P2F_TEST_TOKEN"] = admin_token

# Set the CONSORTIUM USER environment
consortium_user_email = "user@example.com"
consortium_user_token = extract_token(logs=api_container_logs, email=consortium_user_email)

as_consortium_environment = deepcopy(base_environment)
as_consortium_environment["P2F_TEST_EMAIL"] = consortium_user_email
as_consortium_environment["P2F_TEST_TOKEN"] = consortium_user_token


# Set the UNAUTHORIZED USER environment
unauthorized_user_email = "unauthorized@example.com"
unauthorized_user_token = ""

as_unauthorized_environment = deepcopy(base_environment)
as_unauthorized_environment["P2F_TEST_EMAIL"] = unauthorized_user_email
as_unauthorized_environment["P2F_TEST_TOKEN"] = unauthorized_user_token



# Get the most recent client container image
def highest_epoch_seconds(history: List[Dict]) -> int:
    rv = 0
    for h in history:
        if h["Created"] > rv:
            rv = h["Created"]
    return rv

p2f_client_images = client.images.list("p2f-client*")
p2f_client_image_ages = {highest_epoch_seconds(x.history()): x.id.split(":")[-1] for x in p2f_client_images}
p2f_client_image = p2f_client_image_ages[max(p2f_client_image_ages.keys())]

mkdir(f"{getcwd()}/tests/{shtrid}")
# Create the containers
client_portal_container = client.containers.run(image=p2f_client_image,
                                                remove=True,
                                                environment=as_portal_environment,
                                                detach=True,
                                                name=f"p2f_client_test_portal_{str(hex(test_run_id.fields[-1]))[2:]}",
                                                network=api_network)
client_admin_container = client.containers.run(image=p2f_client_image,
                                               remove=True,
                                               environment=as_admin_environment,
                                               detach=True,
                                               name=f"p2f_client_test_admin_{str(hex(test_run_id.fields[-1]))[2:]}",
                                               network=api_network)
client_consortium_container = client.containers.run(image=p2f_client_image,
                                                    remove=True,
                                                    environment=as_consortium_environment,
                                                    detach=True,
                                                    name=f"p2f_client_test_consortium_{str(hex(test_run_id.fields[-1]))[2:]}",
                                                    network=api_network)
client_unauthorized_container = client.containers.run(image=p2f_client_image,
                                                      remove=True,
                                                      environment=as_unauthorized_environment,
                                                      detach=True,
                                                      name=f"p2f_client_test_unauth_{str(hex(test_run_id.fields[-1]))[2:]}",
                                                      network=api_network) 

shtrid = f"{str(hex(test_run_id.fields[-1]))[2:]}"
print([x for x in client.containers.list() if x.name.startswith("p2f_client")])
finished = False
while finished == False:
    client_container_list = [x for x in client.containers.list() if x.name.startswith("p2f_client")]
    for cont in client_container_list:
        try:
            logs_to_write = get_logs_docker(container=cont)
            with open(f"{getcwd()}/tests/{shtrid}/{cont.name}.txt", "w") as f:
                f.write(logs_to_write)
        except docker.errors.NotFound:
            print("container lost")
        except docker.errors.APIError:
            print("API Error")
    sleep(1)
    if len(client_container_list) < 1: 
        finished = True 