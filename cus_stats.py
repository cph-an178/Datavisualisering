import pyodbc
from datetime import datetime

def get_all_orders(cursor, customer_number):
    # This function gets all orderlines from the database
    # and returns a dictionary with an order number as key
    # and a list of orderlines as value
    
    # SQL call which returns OrderNumber, StockCode, UnitPrice, Quantity, OrderDate in a list of lists.
    all_order_lines = cursor.execute("SELECT OR12002, OR12006, OR12009, OR12011, OR12015 FROM OR120100 WHERE OR12016 = '"
                                    + customer_number + "';").fetchall()
    
    # Making sure that we got a result
    if not all_order_lines:
        raise ValueError("Customer number {} didn't return any matches from the datebase".format(customer_number))
    else:
        # Result dictionary
        rs_dict = {}

        # Looping through the list
        for i in all_order_lines:
            # Fixing formating
            i = [i[0], i[1], float(i[2]), float(i[3]), i[4].date().strftime("%B-%Y")]
            if i[0] in [*rs_dict.keys()]: 
                rs_dict[i[0]] += i[1:]
            else:
                rs_dict[i[0]] = i[1:]

        return rs_dict
    