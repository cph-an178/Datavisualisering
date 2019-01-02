import sys
import pyodbc

def connect_to_db(db_connection_file):
    with open(db_connection_file, "r") as file:
        _l = file.read().split(",")
        server = _l[0]
        database = _l[1]
        user = _l[2]
        passwd = _l[3]
    
    conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='
                    +user+';PWD='+passwd)

    return conn.cursor()


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
