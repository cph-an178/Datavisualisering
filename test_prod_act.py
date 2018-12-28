import pytest
import pyodbc
import prod_act as pa
from datetime import datetime

with open("sqlserver.txt", "r") as file:
    _arr = file.read().split(",")
    server = _arr[0]
    database = _arr[1]
    user = _arr[2]
    passwd = _arr[3]

conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='
                    +user+';PWD='+passwd)
cursor = conn.cursor()

# create year dict tests
def test_create_timeframe_dict_currentyear_success():
    timeframe = "currentyear"
    rs_dict = pa.create_timeframe_dict(timeframe)
    rs_dict_keys = [*rs_dict.keys()]
    assert rs_dict_keys[-1] == "December-2018"

def test_create_timeframe_dict_last12months_success():
    timeframe = "last12months"
    rs_dict = pa.create_timeframe_dict(timeframe)
    rs_dict_keys = [*rs_dict.keys()]
    assert rs_dict_keys[-1] == datetime.now().strftime('%B-%Y')

def test_create_timeframe_dict_fail():
    with pytest.raises(ValueError):
        timeframe = "fail"
        pa.create_timeframe_dict(timeframe)

def test_create_prod_act_dict_success():
    search_type = "prod"
    search_number = "342412"
    timeframe = "currentyear"
    rs = pa.create_product_activity_dict(cursor, search_type, search_number, timeframe)
    assert sum([*rs.values()]) > 1000.00

def test_create_prod_cat_act_dict_success():
    search_type = "prod_cat"
    search_number = "101"
    timeframe = "currentyear"
    rs = pa.create_product_activity_dict(cursor, search_type, search_number, timeframe)
    assert sum([*rs.values()]) > 10.00

def test_plot():
    search_type = "prod_cat"
    search_number = "101"
    timeframe = "currentyear"
    rs = pa.create_product_activity_dict(cursor, search_type, search_number, timeframe)
    pa.plot_amount_month(rs, "bar")

