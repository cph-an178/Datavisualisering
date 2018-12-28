import pyodbc
from datetime import datetime
import matplotlib.pyplot as plt

def create_timeframe_dict(timeframe):
    current_date = datetime.now()
    rs_dict = {}
    if timeframe == "currentyear":
        current_year = current_date.year
        for i in range(1, 13):
            rs_dict[datetime(current_year, i, 1).strftime('%B-%Y')] = 0
    elif timeframe == "last12months": 
        starting_month = current_date.month + 1
        starting_year = current_date.year
        for i in range(12):
            if starting_month + i < 12:
                pre_year = starting_year - 1
                rs_dict[datetime(pre_year, starting_month + i, 1).strftime('%B-%Y')] = 0
            else:
                rs_dict[datetime(starting_year, starting_month + i - 12, 1).strftime('%B-%Y')] = 0
    else:
        raise ValueError("timeframe param must either be 'currentyear' or 'last12months")
    
    return rs_dict

def create_product_activity_dict(cursor, search_type, search_number, timeframe):
    # First we create the correct timeframe dict
    rs_dict = create_timeframe_dict(timeframe)

    if search_type == "prod":
        orders = cursor.execute("SELECT OR12011 as quantity," 
                            +"OR12015 as orderdate FROM OR120100 "
                            +"WHERE OR12006 = CONVERT( nvarchar,'" + search_number + "');").fetchall()
        
        for i in orders:
            key = i[1].date().strftime("%B-%Y")
            if key in [*rs_dict.keys()]:
                rs_dict[key] += float(i[0])

    elif search_type == "prod_cat":
        product_list = cursor.execute("SELECT SC01001 as stockcode FROM SC010100 "
                                + "Where SC01037 = CONVERT( nvarchar, " + search_number + ");").fetchall()
    
        product_list = [x[0] for x in product_list]

        for i in product_list:
            orders = cursor.execute("SELECT OR12011 as quantity," 
                            +"OR12015 as orderdate FROM OR120100 "
                            +"WHERE OR12006 = CONVERT( nvarchar,'" + i + "');").fetchall()
        
            for n in orders:
                key = n[1].date().strftime("%B-%Y")
                if key in [*rs_dict.keys()]:
                    rs_dict[key] += float(n[0])

    return rs_dict
    

def plot_amount_month(activity_dict, plot_type):
    if plot_type is "bar":
        plt.bar(range(len(activity_dict)), list(activity_dict.values()))
        plt.xticks(range(len(activity_dict)), list(activity_dict.keys()), rotation='vertical')
    elif plot_type is "plot":
        months = [*activity_dict.keys()]
        amount = [*activity_dict.values()]
        plt.plot(months, amount)
   
    plt.title("Product Activity graph")
    plt.show()