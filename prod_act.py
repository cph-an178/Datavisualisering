from datetime import datetime
import matplotlib.pyplot as plt

def main(cursor, search_type, search_number, timeframe):

    timeframe_dict = create_timeframe_dict(timeframe)

    if search_type == "prod":
        rs_dict = get_orders(cursor, search_number, timeframe_dict)

    elif search_type == "prod_cat":
        rs_dict = get_orders_from_product_list(cursor, search_number, timeframe_dict)

    return rs_dict

def create_timeframe_dict(timeframe):
    current_date = datetime.now()
    timeframe_dict = {}
    if timeframe == "currentyear":
        current_year = current_date.year
        for i in range(1, 13):
            timeframe_dict[datetime(current_year, i, 1).strftime('%B-%Y')] = 0
    elif timeframe == "last12months": 
        starting_month = current_date.month # 1
        starting_year = current_date.year # 2019
        for i in range(1, 13):
            if starting_month + i <= 12:
                pre_year = starting_year - 1
                timeframe_dict[datetime(pre_year, starting_month + i, 1).strftime('%B-%Y')] = 0
            else:
                timeframe_dict[datetime(starting_year, starting_month + i - 12, 1).strftime('%B-%Y')] = 0
    
    return timeframe_dict
    
def get_orders(cursor, product_nr, timeframe_dict):
    # SQL call that returns Quantity and Order date
    orders = cursor.execute("SELECT OR12011, OR12015 FROM OR120100 WHERE OR12006 = CONVERT( nvarchar,'" 
                            + product_nr + "');").fetchall()
    
    if not orders:
        raise ValueError("Could not find any product with product number {}".format(product_nr))
    else:
        for i in orders:
            key = i[1].date().strftime("%B-%Y")
            if key in [*timeframe_dict.keys()]:
                timeframe_dict[key] += float(i[0])
        
        return timeframe_dict

def get_orders_from_product_list(cursor, product_cat, timeframe_dict):
    product_list = cursor.execute("SELECT SC01001 as stockcode FROM SC010100 "
                                + "Where SC01037 = CONVERT( nvarchar, " + product_cat + ");").fetchall()
    
    if not product_list:
        raise ValueError("Could not find any product category with number {}".format(product_cat))
    else:
        product_list = [x[0] for x in product_list]

        for i in product_list:
            orders = cursor.execute("SELECT OR12011 as quantity," 
                            +"OR12015 as orderdate FROM OR120100 "
                            +"WHERE OR12006 = CONVERT( nvarchar,'" + i + "');").fetchall()

            for n in orders:
                key = n[1].date().strftime("%B-%Y")
                if key in [*timeframe_dict.keys()]:
                    timeframe_dict[key] += float(n[0])

        return timeframe_dict

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