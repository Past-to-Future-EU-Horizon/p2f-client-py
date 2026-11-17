from random import randint, choice
from secrets import token_urlsafe
from p2f_client.p2f_client import P2F_Client
from logger_tests import logger
from report_result import add_report
from test_admincheat import get_random_existing_uuid

def insert_datatype(client: P2F_Client):
    logger.debug("Running insert datatype")
    new_datatype = client.harm_data_type.data_model(
        measure=choice(["CO2 Concentration", "Voltage", "Power", "Fecundity", "Distance", "Force"]),
        unit_of_measurement=choice(["Index", "Mols", "Volts", "Watts", "Newtons", "Meters", "Centimeters", "Kilometers"]),
        method=choice(["Direct measurement", "Wind Vane", "Taste Test", "Potentiometer", "Cyanamometer", "Wireless"]),
        calibration=choice(["None", "Finger in the wind", "Erasmus et. al., 1534", "We asked the dataset how it felt", "Emmentaller 2020"]),
        is_proxy=choice([True, False])
    )
    logger.debug("Created datatype, trying to insert")
    try: 
        new_datatype = client.harm_data_type.upload_data_type(new_data_type=new_datatype)
        add_report(test_name="INSERT DATA TYPE", output_text=new_datatype.model_dump_json(exclude_unset=True), status_code=100)
        logger.debug(f"New data type: {new_datatype.model_dump_json(exclude_unset=True)}")
    except Exception as e:
        add_report(test_name="INSERT DATA TYPE", output_text=e, status_code=999)

def list_datatypes(client: P2F_Client):
    logger.debug("Running list datatypes")
    try:
        datatype_list = client.harm_data_type.list_data_types()
        logger.debug("Listed data types")
        add_report(test_name="LIST DATA TYPES", output_text=f"Number of data types: {len(datatype_list)}", status_code=100)
    except Exception as e:
        logger.debug(f"Error with inserting data type: {e}")
        add_report(test_name="LIST DATA TYPES", output_text=e, status_code=999)

def delete_datatype(client: P2F_Client):
    datatype_to_delete = get_random_existing_uuid("datatype")
    try: 
        client.harm_data_type.delete_data_type(datatype_to_delete)
        add_report(test_name="DELETE DATA TYPE", output_text="datatype deleted", status_code=100)
    except Exception as e:
        add_report(test_name="DELETE DATA TYPE", output_text=e, status_code=999)