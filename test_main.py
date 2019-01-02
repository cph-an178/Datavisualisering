import os
import main
import pyodbc
import pytest

def test_connect_to_db_success():
    cursor = main.connect_to_db("sqlserver.txt")
    rs = cursor.execute("select top 1 * from SC010100").fetchone()
    assert rs != None

def test_connect_to_db_no_file_fail():
    with pytest.raises(FileNotFoundError):
        main.connect_to_db("fail.txt")
