import pyodbc
import datetime
import matplotlib.pyplot as plt

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
        prod_list = cursor.execute("SELECT CONVERT( nchar, OR03001) as ordernr," 
                            +"CONVERT(float, OR03011) as amount FROM OR030100 "
                            +"WHERE OR03005 = CONVERT( nvarchar,'" + search_number + "');").fetchall()

        for i in prod_list:
            od = cursor.execute("SELECT OR01002 as orderType, OR01015 as orderDate FROM OR010100 WHERE OR01001 = "
                            + i[0] +";").fetchone()
            if od != None:
                date = od[1].date().strftime("%d-%m-%Y")
                rs_dict.update({date:i[1]})

    # If it's a product groupe
    else: 
        prod_cat = cursor.execute("SELECT CONVERT( nchar, SC01001) as artnr FROM SC010100 "
                            +"WHERE SC01037  = CONVERT( nvarchar,'" + search_number + "');").fetchall()

        for i in prod_cat:
            i[0] = i[0].strip()
            prod_list = cursor.execute("SELECT CONVERT( nchar, OR03001) as ordernr," 
                            +"CONVERT(float, OR03011) as amount FROM OR030100 "
                            +"WHERE OR03005 = CONVERT( nvarchar, '" + i[0] + "');").fetchall()

            for n in prod_list:
                n[0] = n[0].strip()
                
                od = cursor.execute("SELECT OR01002 as orderType, OR01015 as orderDate FROM OR010100 WHERE OR01001 = "
                            +"CONVERT( nvarchar, '" + n[0].strip() +"');").fetchone()

                if od != None:
                    date = od[1].date().strftime("%d-%m-%Y")
                    rs_dict.update({date:n[1]})
    
    return rs_dict

def map_amount_to_month(date_amount_dict, annual_boolean):

    rs_dict = {}
    if annual_boolean:
        # Dictionary for every month
        rs_dict = {'Jan':0, 'Feb': 0, 'Mar': 0, 'Apr': 0, 'May': 0, 'Jun': 0, 'Jul': 0, 'Aug': 0, 'Sep': 0, 'Oct':0, 'Nov': 0, 'Dec':0}
        for e in date_amount_dict:
            e_split = e.split('-')
            e_split = [int(e) for e in e_split]
            e_year = datetime.datetime(e_split[2], e_split[1], e_split[0]).year
            if e_year == datetime.datetime.now().year:
                m = datetime.datetime(e_split[2], e_split[1], e_split[0]).strftime('%b')
                rs_dict[m] += float(e[1])

    else:
        # Generating dictionany going back 12 months from today
        starting_month = datetime.datetime.now().month + 1
        for i in range(12):
            if starting_month + i < 12:
                pre_month = datetime.datetime(2018, starting_month + i, 1).strftime('%b')
                rs_dict.update({pre_month: 0})
            else:
                pre_month = datetime.datetime(2018, starting_month + i - 12, 1).strftime('%b')
                rs_dict.update({pre_month: 0})

        for e in date_amount_dict:
            e_split = e.split('-')
            e_split = [int(e) for e in e_split]
            e_year = datetime.datetime(e_split[2], e_split[1], e_split[0]).year
            if e_year == datetime.datetime.now().year:
                m = datetime.datetime(e_split[2], e_split[1], e_split[0]).strftime('%b')
                rs_dict[m] += float(e[1])

    return rs_dict

def plot_amount_month(year_amount_dict):
    months = list(year_amount_dict.keys())
    amount = list(year_amount_dict.values())
    plt.plot(months, amount)
    # plt.plot(range(len(year_amount_dict)), list(year_amount_dict.values()), align='center')
    # plt.xticks(range(len(year_amount_dict)), list(year_amount_dict.keys()))
    plt.show()