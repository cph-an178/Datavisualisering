import main
import pyodbc

def test_conn():
    with open("sqlserver.txt", "r") as file:
        _arr = file.read().split(",")
        server = _arr[0]
        database = _arr[1]
        user = _arr[2]
        passwd = _arr[3]
    conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+user+';PWD='+passwd)
    re = conn.cursor().execute("SELECT * FROM SC010100").fetchone()

    assert re != None

def test_create_date_amount_product():
    """
        This test that we create an dictonary that adds a date as key
        and a amount sold as a value
    """
    artnr = "342412" # Product number
    date_amount_dict = main.create_date_amount_dict(artnr)
    # We know that the dictionary's length should be larger than 0
    assert len(date_amount_dict) != 0

def test_create_date_amount_prod_group():
    """
        This test makes sure that our create_date_amount_dict function
        can also create an dictionary of a product group
    """
    product_group = "101"
    date_amount_dict = main.create_date_amount_dict(product_group)
    assert len(date_amount_dict) != 0

def test_map_amount_to_month_annual():
    """
        This test makes sure that the function can map the amount from a
        dictionay to the corresponding month for current year jan-dec
    """
    # This dictionary is from test_create_Date_amount_prod_group
    test_dict = {'10-10-2014': 217.0, '26-04-2017': 21.0, '12-06-2018': 900.0, '07-11-2018': 30.0, '06-06-2018': 10.0, '29-08-2018': 30.0, '12-11-2018': 4.0, '01-11-2018': 29.0, '25-10-2018': 1.0, '27-10-2010': 1.0, '06-11-2018': 10.0, '24-10-2018': 20.0, '07-08-2014': 94.0, '10-09-2018': 12.0, '29-10-2018': 400.0, '05-11-2010':
1.0, '13-04-2011': 1.0, '23-10-2015': 10.0}

    rs_dict = main.map_amount_to_month(test_dict, True)
    assert len(rs_dict) == 12

def test_map_amount_to_month_yearback():
    """
        This test makes sure that the function can map the amount from a
        dictionay to the corresponding month for current year jan-dec
    """
    # This dictionary is from test_create_Date_amount_prod_group
    test_dict = {'10-10-2014': 217.0, '26-04-2017': 21.0, '12-06-2018': 900.0, '07-11-2018': 30.0, '06-06-2018': 10.0, '29-08-2018': 30.0, '12-11-2018': 4.0, '01-11-2018': 29.0, '25-10-2018': 1.0, '27-10-2010': 1.0, '06-11-2018': 10.0, '24-10-2018': 20.0, '07-08-2014': 94.0, '10-09-2018': 12.0, '29-10-2018': 400.0, '05-11-2010':
1.0, '13-04-2011': 1.0, '23-10-2015': 10.0}

    rs_dict = main.map_amount_to_month(test_dict, False)
    assert len(rs_dict) == 12

def test_year_dict_plot():
    # This dictionay is from test_map_amount_to_month_yearback
    year_dict = {'Jan': 0, 'Feb': 0, 'Mar': 0, 'Apr': 0, 'May': 0, 'Jun': 8.0, 'Jul': 0, 'Aug': 9.0, 'Sep': 0.0, 'Oct': 18.0, 'Nov': 16.0, 'Dec': 0}
    main.plot_amount_month(year_dict)