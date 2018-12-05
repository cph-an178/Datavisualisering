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