import sys
import pyodbc
import argparse
import modules.prod_act as pa

def connect_to_db(db_connection_file):
    # Denne metode tager en parameter som skal være
    # en tekstfil med information til den database
    # man vil have forbindelse til.

    # Vi bruger with open til til at læse filen og
    # giver en en extra parameter "r" som betyder 'read'
    # Det gør at den kun læser filen og kan ikke skrive
    # til den.
    with open(db_connection_file, "r") as file:

        # Vi læser filen og splitter den fra kommaerne
        # og laver en liste af resultatet
        _l = file.read().split(",")

        # Derefter laver vi de variabler vi skal bruge
        # for at komme på en SQL server og tildeler dem
        # elemterne fra listen
        server = _l[0]
        database = _l[1]
        user = _l[2]
        passwd = _l[3]
    
    # Så bruger vi pyodbc's connect funktion parse en SQL
    # Connection String med vores variabler indsat de
    # korrekte steder
    conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='
                    +user+';PWD='+passwd)

    # Til sidst retunere vi et cursor objekt som man kan
    # bruge til at lave SQL kald til databasen
    return conn.cursor()

def main():
    # Vi kunne godt tænke os at programmet virker ligesom rigtige
    # Python programmer. Derfor vil vi bruge biblioteket 'argparse'
    # til at kunne køre forskellige dele af programmet ud fra hvilke
    # system arguments den får

    # Først laver en en ArgumentParser
    parser = argparse.ArgumentParser()

    # Derefter tilføjer vi de to Arguments vi gerne vil kunne køre
    parser.add_argument("-cs", "--customer_statistics", help="To get statistics for an customer", action="store_true")
    parser.add_argument("-pa", "--product_activity", help="To get info about product or product category activity", action="store_true")
    # Vi giver dem en kort argument med en "-" og en lang argument med "--"
    # Vi giver også hver argument en hjælpe tekst til at forklare hvad de gør
    # Til sidste giver vi dem en action "store_true" så vi kan kalde dem
    # Senere i koden

    # Vi parser vores nye arguments
    args = parser.parse_args()

    # Vores metoder skal bruge en pyodbc cursor så vi laver en variable
    # der kalder vores connect_to_db metode med en textfil sti
    cursor = connect_to_db("sqlserver.txt")

    # Vi laver nogle tjek på om programmet for de rigtige arguments
    if args.customer_statistics:
        # Hvis man skrev "-ca" eller "--customer_statistics" køre vi denne
        # funtion
        customer_statistics(cursor)
    elif args.product_activity:
        # Eller hvis man skrev "-ca" eller "--customer_statistics" køre vi 
        # denne funtion
        product_activity(cursor)
    else:
        # Hvis man ikke giver noget argument eller et der ikke findes
        # printer vi en hjælpe beksed
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
        
        # Efter vi har fået vores search_type, search_number og
        # timeframe laver vi en try/expect blok
        try:
            # Først prøver den at kalde main metoden i prod_act.py
            rs_dict = pa.main(cursor, search_type,search_number, timeframe)
        except ValueError as e:
            # Hvis den får en ValueError printer den fejlen så brugen
            # kan se hvad der gik galt
            print(e)
            # Derefter ændre den restart boolean'en så metoden køre
            # igen
            should_restart = True
        else:
            # Hvis den ikke får en ValueError plotter den resultatet
            # den fik fra main metoden
            pa.plot_amount_month(rs_dict, 'bar')

if __name__ == "__main__":
    main()