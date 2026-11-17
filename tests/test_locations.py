from random import randint, choice, random
from secrets import token_urlsafe
from p2f_client.p2f_client import P2F_Client
from logger_tests import logger
from report_result import add_report
from test_utils import create_random_lat, create_random_lon, create_random_float
from test_admincheat import get_random_existing_uuid

def insert_location(client: P2F_Client):
    location_code = token_urlsafe(64)[:5]
    new_location = client.harm_location.data_model(
        location_name=f"{client.auth_email} Location {location_code}",
        location_code=location_code, 
        latitude=create_random_lat(),
        longitude=create_random_lon(),
        elevation=create_random_float(-1000, 5000),
        location_age=choice([0,0,0,0,0,0, randint(0, 5_000_000)])
    )
    logger.debug(f"Trying to insert the location {new_location.model_dump_json(exclude_unset=True)}")
    try: 
        new_location = client.harm_location.upload_harm_location(new_location=new_location)
        logger.debug("Inserted the new location")
        add_report(test_name="INSERT LOCATION", output_text=new_location.model_dump_json(exclude_unset=True), status_code=100)
    except Exception as e:
        logger.debug(f"Insert of location failed with message {e}")
        add_report(test_name="INSERT LOCATION", output_text=e, status_code=999)

def list_locations(client: P2F_Client):
    logger.debug("Trying to read locations from API")
    try:
        location_list = client.harm_location.list_harm_locations()
        logger.debug(f'Successfully listed {len(location_list)} locations from the API')
        add_report(test_name="LIST LOCATION", output_text=f"Location list length {len(location_list)}", status_code=100)
    except Exception as e:
        logger.debug(f"Location listing failed with the message {e}")
        add_report(test_name="LIST LOCATION", output_text=e, status_code=999)

def delete_location(client: P2F_Client):
    location_to_delete = get_random_existing_uuid("location")
    logger.debug(f"Trying to delete location {location_to_delete}")
    try:
        client.harm_location.delete_harm_location(location_id=location_to_delete)
        logger.debug("Successfully deleted the location")
        add_report(test_name="DELETE LOCATION", output_text="location deleted", status_code=100)
    except Exception as e:
        logger.debug(f"Failed to delete location with error {e}")
        add_report(test_name="DELETE LOCATION", output_text=e, status_code=999)