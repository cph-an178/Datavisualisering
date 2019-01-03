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
    print(rs_dict)
    assert rs_dict_keys[-1] == ("December-" + datetime.now().strftime('%Y'))

# FAILS, Need to revisit in 2019
def test_create_timeframe_dict_last12months_success():
    timeframe = "last12months"
    rs_dict = pa.create_timeframe_dict(timeframe)
    rs_dict_keys = [*rs_dict.keys()]
    assert rs_dict_keys[-1] == datetime.now().strftime('%B-%Y')

def test_get_orders_success():
    timeframe_dict = {'January-2018': 0, 'February-2018': 0, 'March-2018': 0, 'April-2018': 0, 'May-2018': 0, 'June-2018': 0, 'July-2018': 0, 'August-2018': 0, 'September-2018': 0, 'October-2018': 0, 'November-2018': 0, 'December-2018': 0}
    product_nr = "342412"
    rs = pa.get_orders(cursor, product_nr, timeframe_dict)
    assert sum([*rs.values()]) > 1000.00

def test_get_orders_fail():
    timeframe_dict = {'January-2018': 0, 'February-2018': 0, 'March-2018': 0, 'April-2018': 0, 'May-2018': 0, 'June-2018': 0, 'July-2018': 0, 'August-2018': 0, 'September-2018': 0, 'October-2018': 0, 'November-2018': 0, 'December-2018': 0}
    product_nr = "fail"
    with pytest.raises(ValueError):
        pa.get_orders(cursor, product_nr, timeframe_dict)

def test_get_orders_from_product_list_success():
    timeframe_dict = {'January-2018': 0, 'February-2018': 0, 'March-2018': 0, 'April-2018': 0, 'May-2018': 0, 'June-2018': 0, 'July-2018': 0, 'August-2018': 0, 'September-2018': 0, 'October-2018': 0, 'November-2018': 0, 'December-2018': 0}
    product_cat = "101"
    rs = pa.get_orders_from_product_list(cursor, product_cat, timeframe_dict)
    assert sum([*rs.values()]) > 10.00

def test_get_orders_from_product_list_fail():
    timeframe_dict = {'January-2018': 0, 'February-2018': 0, 'March-2018': 0, 'April-2018': 0, 'May-2018': 0, 'June-2018': 0, 'July-2018': 0, 'August-2018': 0, 'September-2018': 0, 'October-2018': 0, 'November-2018': 0, 'December-2018': 0}
    product_cat = "9999"
    with pytest.raises(ValueError):
        pa.get_orders_from_product_list(cursor, product_cat, timeframe_dict)

""" Tests somehow breaks ???
def test_main_prod_success():
    search_type = "prod"
    search_number = "342412"
    timeframe = {'January-2018': 0, 'February-2018': 0, 'March-2018': 0, 'April-2018': 0, 'May-2018': 0, 'June-2018': 0, 'July-2018': 0, 'August-2018': 0, 'September-2018': 0, 'October-2018': 0, 'November-2018': 0, 'December-2018': 0}
    rs = pa.main(cursor, search_type, search_number, timeframe)
    assert sum([*rs.values()]) > 1000.00

def test_main_prod_cat_success():
    search_type = "prod_cat"
    search_number = "101"
    timeframe = {'January-2018': 0, 'February-2018': 0, 'March-2018': 0, 'April-2018': 0, 'May-2018': 0, 'June-2018': 0, 'July-2018': 0, 'August-2018': 0, 'September-2018': 0, 'October-2018': 0, 'November-2018': 0, 'December-2018': 0}
    rs = pa.main(cursor, search_type, search_number, timeframe)
    assert sum([*rs.values()]) > 10.00
"""
def test_plot():
    activity_dict = {'January-2018': 460, 'February-2018': 510, 'March-2018': 750, 'April-2018': 132, 'May-2018': 608, 'June-2018': 423, 'July-2018': 864, 'August-2018': 341, 'September-2018': 563, 'October-2018': 973, 'November-2018': 145, 'December-2018': 52}
    plot_type = "bar"
    pa.plot_amount_month(activity_dict, plot_type)

