import main
import pyodbc

def test_conn():
    with open("sqlserver.txt", "r") as file:
        _arr = file.read().split(",")
        server = _arr[0]
        database = _arr[1]
        user = _arr[2]
        passwd = _arr[3]
    conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+user+';PWD='+passwd)
    re = conn.cursor().execute("SELECT * FROM SC010100").fetchone()

    assert re != None

def test_create_date_amount_product():
    """
        This test that we create an dictonary that adds a date as key
        and a amount sold as a value
    """
    artnr = "342412" # Product number
    date_amount_dict = main.create_date_amount_dict(artnr)
    # We know that the dictionary's length should be larger than 0
    assert len(date_amount_dict) != 0

def test_create_date_amount_prod_groupe():
    """
        This test makes sure that our create_date_amount_dict function
        can also create an dictionary of a product group
    """
    product_group = "101"
    date_amount_dict = main.create_date_amount_dict(product_group)
    assert len(date_amount_dict) != 0