from random import randint, choice, random
from secrets import token_urlsafe
import uuid
from p2f_client.p2f_client import P2F_Client
from logger_tests import logger
from report_result import add_report
from test_admincheat import get_random_existing_uuid
from test_utils import create_random_float
import pandas as pd

def create_dataset(client: P2F_Client, n=100):
    dataset_id = get_random_existing_uuid("dataset")
    df = pd.DataFrame(columns=["float_value", "int_value", 
                               "float_m", "float_uv", "float_ui", "float_lv", "float_li",
                               "int_m", "int_uv", "int_ui", "int_lv", "int_li"])
    frange = [randint(-2000, 2000), randint(-2000, 2000)]
    irange = [randint(-2000, 2000), randint(-2000, 2000)]
    fcrange = [randint(-2000, 2000), randint(-2000, 2000)]
    icrange = [randint(-2000, 2000), randint(-2000, 2000)]

    for i in range(n):
        fv = create_random_float(lower=min(frange), upper=max(frange))
        iv = randint(min(irange), max(irange))
        fm = create_random_float(lower=min(fcrange), upper=max(fcrange))
        fuv = fm + (fm*random())
        flv = fm - (fm*random())
        fui, fli = choice([95, 97.5]), choice([2.5, 5])
        im = randint(min(icrange), max(icrange))
        iuv = im + (im*random())
        ilv = im - (im*random())
        iuv, ilv = int(iuv), int(iuv)
        iui, ili = choice([95, 97.5]), choice([2.5, 5])
        df.loc[i] = (fv, iv,
                     fm, fuv, fui, flv, fli,
                     im, iuv, iui, ilv, ili)
    df["record_hash"] = [client.harm_data_records.calculate_hash(dataset_id=dataset_id, row_number=x) for x in df.index]
    idt, icdt, fdt, fcdt = get_random_existing_uuid("datatype"), get_random_existing_uuid("datatype"), get_random_existing_uuid("datatype"), get_random_existing_uuid("datatype")
    for ix, rec in df.iterrows():
        try:
            new_record_hash = client.harm_data_records.data_model(fk_dataset=dataset_id, record_hash=rec.record_hash)
            new_record_hash = client.harm_data_records.upload_data_record(new_record_hash)
            add_report(test_name="ADD RECORD HASH", output_text=new_record_hash.model_dump_json(exclude_unset=True), status_code=100)
        except Exception as e:
            add_report(test_name="ADD RECORD HASH", output_text=e, status_code=999)
        insert_int(client=client, record_hash=rec.record_hash, datatype=idt, int_value=rec.int_value)
        insert_float(client=client, record_hash=rec.record_hash, datatype=fdt, float_value=rec.float_value)
        insert_int_confidence(client=client, record_hash=rec.record_hash, datatype=icdt, 
                              int_value=rec.int_m, int_upper_value=rec.int_uv, int_lower_value=rec.int_lv, int_upper_conf=rec.int_ui, int_lower_conf=rec.int_li)
        insert_float_confidence(client=client, record_hash=rec.record_hash, datatype=fcdt,
                                float_value=rec.float_m, float_upper_value=rec.float_uv, float_lower_value=rec.float_lv, float_upper_conf=rec.float_ui, float_lower_conf=rec.float_li)


        
def insert_int(client: P2F_Client, record_hash: str, datatype: uuid.UUID,
               int_value: int):
    new_numeric = client.harm_numerical.data_model(fk_data_record=record_hash, 
                                                   fk_data_type=datatype,
                                                   numerical_type="INT",
                                                   value=int_value)
    try:
        new_numeric = client.harm_numerical.upload_harm_numerical(new_record=new_numeric)
        add_report(test_name="INSERT NUMERIC INT", output_text=new_numeric.model_dump_json(exclude_unset=True), status_code=100)
    except Exception as e:
        add_report(test_name="INSERT NUMERIC INT", output_text=e, status_code=999)

def insert_float(client: P2F_Client, record_hash: str, datatype: uuid.UUID,
                 float_value: float):
    new_numeric = client.harm_numerical.data_model(fk_data_record=record_hash,
                                                   fk_data_type=datatype,
                                                   numerical_type="FLOAT", 
                                                   value=float_value)
    try:
        new_numeric = client.harm_numerical.upload_harm_numerical(new_record=new_numeric)
        add_report(test_name="INSERT NUMERIC FLOAT", output_text=new_numeric.model_dump_json(exclude_unset=True), status_code=100)
    except Exception as e:
        add_report(test_name="INSERT NUMERIC FLOAT", output_text=e, status_code=999)

def insert_int_confidence(client: P2F_Client, record_hash: str, datatype: uuid.UUID,
                          int_value: int, int_upper_value, int_lower_value,
                          int_upper_conf, int_lower_conf):
    new_numeric = client.harm_numerical.data_model(fk_data_record=record_hash, 
                                                   fk_data_type=datatype,
                                                   numerical_type="INT",
                                                   value=int_value,
                                                   upper_conf_value=int_upper_value, 
                                                   upper_conf_interval=int_upper_conf,
                                                   lower_conf_value=int_lower_value, 
                                                   lower_conf_interval=int_lower_conf)
    try:
        new_numeric = client.harm_numerical.upload_harm_numerical(new_record=new_numeric)
        add_report(test_name="INSERT NUMERIC INT CONF", output_text=new_numeric.model_dump_json(exclude_unset=True), status_code=100)
    except Exception as e:
        add_report(test_name="INSERT NUMERIC INT CONF", output_text=e, status_code=999)

def insert_float_confidence(client: P2F_Client, record_hash: str, datatype: uuid.UUID,
                 float_value: float, float_upper_value, float_lower_value,
                 float_upper_conf, float_lower_conf):
    new_numeric = client.harm_numerical.data_model(fk_data_record=record_hash,
                                                       fk_data_type=datatype,
                                                       numerical_type="FLOAT", 
                                                       value=float_value,
                                                       upper_conf_value=float_upper_value, 
                                                       upper_conf_interval=float_upper_conf,
                                                       lower_conf_value=float_lower_value,
                                                       lower_conf_interval=float_lower_conf)
    try:
        new_numeric = client.harm_numerical.upload_harm_numerical(new_record=new_numeric)
        add_report(test_name="INSERT NUMERIC FLOAT CONF", output_text=new_numeric.model_dump_json(exclude_unset=True), status_code=100)
    except Exception as e:
        add_report(test_name="INSERT NUMERIC FLOAT CONF", output_text=e, status_code=999)