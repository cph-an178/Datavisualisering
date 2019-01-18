import pyodbc

class DbConn:
    def __init__(self, db_connection_file):
        with open(db_connection_file, "r") as file:
            _l = file.split(",")

            server = _l[0]
            database = _l[1]
            user = _l[2]
            passwd = _l[3]

        connection_string = (r"DRIVER={ODBC Driver 17 for SQL Server};SERVER={0}"
                            ";DATABASE={1};UID={2};PWD={3}").format(server, 
                                database, user, passwd)

        conn =  pyodbc.connect(connection_string)

        self.cursor = conn.cursor()

    def get_orders_by_product_number(self, product_number):
        orders = self.cursor.execute("SELECT OR12011 as qty, OR12015 as dato FROM "
                            + "OR120100 WHERE OR12006 = CONVERT( nvarchar,'" 
                            + product_number + "');").fetchall()

        return orders

    def get_products_by_product_category_number(self, product_category_number):
        products = self.cursor.execute("SELECT SC01001 as stockcode FROM SC010100 "
                                + "Where SC01037 = CONVERT( nvarchar, " 
                                + product_category_number + ");").fetchall()

        return products