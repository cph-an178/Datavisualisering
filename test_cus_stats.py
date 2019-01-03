import pyodbc
import pytest
import cus_stats as cs

with open("sqlserver.txt", "r") as file:
    _arr = file.read().split(",")
    server = _arr[0]
    database = _arr[1]
    user = _arr[2]
    passwd = _arr[3]

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
    pass