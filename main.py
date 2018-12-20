import pyodbc
import datetime

with open("sqlserver.txt", "r") as file:
    _arr = file.read().split(",")
    server = _arr[0]
    database = _arr[1]
    user = _arr[2]
    passwd = _arr[3]

conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='
                    +user+';PWD='+passwd)
cursor = conn.cursor()

supplies_table = cursor.execute("SELECT * FROM SC010100").fetchall()

def create_date_amount_dict(search_number):
    """
        This function creates a dictionary of a givin product or
        product group with the ordered date as key and the amount as the value
    """
    # Empty result dictionary
    rs_dict = {}

    # If it's an product number
    if len(search_number) > 4:
        prod_list = cursor.execute('SELECT CONVERT( nchar, OR03001) as ordernr,' 
                            +'CONVERT(float, OR03011) as amount FROM OR030100 '
                            +'WHERE OR03005 = CONVERT( nvarchar,' + search_number + ');').fetchall()

        for i in prod_list:
            od = cursor.execute('SELECT OR01002 as orderType, OR01015 as orderDate FROM OR010100 WHERE OR01001 = '
                            + i[0] +';').fetchone()
            if od != None:
                date = od[1].date().strftime("%d-%m-%Y")
                rs_dict.update({date:i[1]})

    # If it's a product groupe
    else: 
        prod_cat = cursor.execute('SELECT CONVERT( nchar, SC01001) as artnr FROM SC010100 '
                            +'WHERE SC01037  = CONVERT( nvarchar,' + search_number + ');').fetchall()
        print("Product cat list : ", prod_cat[:1])
        for i in prod_cat:
            i[0] = i[0].strip()
            prod_list = cursor.execute('SELECT CONVERT( nchar, OR03001) as ordernr,' 
                            +'CONVERT(float, OR03011) as amount FROM OR030100 '
                            +'WHERE OR03005 = CONVERT( nvarchar,' + i[0] + ');').fetchall()
            print("Product list : ", prod_list)
            for n in prod_list:
                n[0] = n[0].strip()
                print("Product : ", n)
                
                od = cursor.execute('SELECT OR01002 as orderType, OR01015 as orderDate FROM OR010100 WHERE OR01001 = '
                            +'CONVERT( nvarchar, ' + n[0].strip() +');').fetchone()
                if od != None:
                    date = od[1].date().strftime("%d-%m-%Y")
                    rs_dict.update({date:n[1]})
    

    return rs_dict