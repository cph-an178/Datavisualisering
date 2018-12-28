import sys
import pyodbc

def connect_to_db(db_connection_file):
    with open(db_connection_file, "r") as file:
        _arr = file.read().split(",")
        server = _arr[0]
        database = _arr[1]
        user = _arr[2]
        passwd = _arr[3]
    
    conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='
                    +user+';PWD='+passwd)

    return conn.cursor()


def dummy_def(cursor, sql_table, sql_row,search_num):
    rs = cursor.execute("SELECT TOP 5 * FROM " + sql_table + " WHERE " + sql_row + " ='" + search_num + "'").fetchall()
    return rs


def main():
    cursor = connect_to_db("sqlserver.txt")
    sql_table = sys.argv[1] # "SC010100"
    sql_row = sys.argv[2] # "SC01001"
    search_num = sys.argv[3] # "342412"
    rs_list = dummy_def(cursor, sql_table, sql_row, search_num)
    for i in rs_list:
        print(i)


if __name__ == "__main__":
    main()
