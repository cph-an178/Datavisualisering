import pyodbc

conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-9JD28UO;DATABASE=iScalaDB;UID=db_reader;PWD=sqlPoli10et')
cursor = conn.cursor()

supplies_table = cursor.execute("SELECT * FROM SC010100").fetchall()

print(supplies_table[0])
