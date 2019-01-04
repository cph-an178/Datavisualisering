import sys
import pyodbc
import argparse
import prod_act as pa

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
    # First we create Argparse to help guide users
    # for how to use our program
    parser = argparse.ArgumentParser()
    parser.add_argument("-cs", "--customer_statistics", help="To get statistics for an customer", action="store_true")
    parser.add_argument("-pa", "--product_activity", help="To get info about product or product category activity", action="store_true")
    args = parser.parse_args()

    cursor = connect_to_db("sqlserver.txt")

    if args.customer_statistics:
        customer_statistics(cursor)
    if args.product_activity:
        product_activity(cursor)
    else:
        print("Use -h or --help for help with this program")

def customer_statistics(cursor):
    print("This task is not completed yet")

def product_activity(cursor):
    print("In this function you can get a graph of monthly activity \n"
            + "of either a product or a product category.")
    should_restart = True
    while should_restart:
        should_restart = False
        print("Type 1 if you want to search for a product \n"
            + "Type 2 if you want to search for a product category")
        
        _input1 = input()

        if _input1 is '1':
            search_type = 'prod'
            print("Which product code do you wish to search for?")
            search_number = input()
        elif _input1 is '2':
            search_type = 'prod_cat'
            print("Which product category code do you wish to search for?")
            search_number = input()
        else:
            print("You need to either type 1 or 2")
            should_restart = True
            break

        print("What kind of timeframe do you wish for? \n"
            + "Type 1 for current year \n"
            + "Type 2 for last 12 months")

        _input2 = input()

        if _input2 is '1':
            timeframe = 'currentyear'
        elif _input2 is '2':
            timeframe = 'last12months'
        else:
            should_restart = True
            break
        
        try:
            rs_dict = pa.main(cursor, search_type,search_number, timeframe)
        except ValueError as e:
            print(e)
            should_restart = True
        else:
            pa.plot_amount_month(rs_dict, 'bar')

if __name__ == "__main__":
    main()