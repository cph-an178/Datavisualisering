import pyodbc

def test_conn():

    server = "DESKTOP-9JD28UO"
    database = "iScalaDB"
    user = "db_reader"
    passwd = "sqlPoli10et"

    conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+user+';PWD='+passwd)
    cursor = conn.cursor()

    supplies_table = cursor.execute("SELECT * FROM SC010100").fetchall()

    assert len(supplies_table) != 0