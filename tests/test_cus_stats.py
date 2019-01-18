import pyodbc
import pytest
import modules.cus_stats as cs

with open("sqlserver.txt", "r") as file:
    _l = file.read().split(",")
    server = _l[0]
    database = _l[1]
    user = _l[2]
    passwd = _l[3]

conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='
                    +user+';PWD='+passwd)
cursor = conn.cursor()

def test_get_all_orders_success():
    customer_number = '0241'
    rs = cs.get_all_orders(cursor, customer_number)
    assert len([*rs.keys()]) > 1000 # We know from MSSQLSMS that there should be more than 1000 orders

def test_get_all_orders__fail():
    customer_number = 'fail'
    with pytest.raises(ValueError):
        cs.get_all_orders(cursor, customer_number)
    

def test_get_most_active_months_success():
    # OrderNumber, StockCode, UnitPrice, Quantity, OrderDate
    orders_dict = {'0001': ['342412', 20.0, 4.0, 'January-2018'], '0002': ['342412', 20.0, 4.0, 'January-2018'], '0003': ['342412', 20.0, 4.0, 'January-2018'],
                '0004': ['342412', 20.0, 4.0, 'February-2018'], '0005': ['342412', 20.0, 4.0, 'February-2018'], '0006': ['342412', 20.0, 4.0, 'March-2018']}
    rs = cs.get_most_active_months(orders_dict)
    assert rs['January'] is 3
    assert rs['February'] is 2
    assert rs['March'] is 1

def test_get_most_popular_product_success():
    orders_dict = {'0001': ['342412', 20.0, 4.0, 'January-2018'], '0002': ['342412', 20.0, 4.0, 'January-2018'], '0003': ['342412', 20.0, 4.0, 'January-2018'],
                '0004': ['342412', 20.0, 4.0, 'February-2018'], '0005': ['342412', 20.0, 4.0, 'February-2018'], '0006': ['342412', 20.0, 4.0, 'March-2018']}
    pass

def test_main_active_months_success():
    pass

def test_main_popular_product_success():
    pass

