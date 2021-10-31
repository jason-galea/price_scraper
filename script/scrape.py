#!/usr/bin/python3

### Imports
import time
from typing import Dict
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from mysql import connector
from mysql.connector import errorcode as err


### Constants
SQL_USER = "scraper"
SQL_PASS = "Password##123"
SQL_DB = "PriceScraper"
SQL_TABLES = {
    "HDD": "Time DATETIME, \
    Retailer varchar(255), \
    Title varchar(255), \
    URL varchar(255), \
    PriceAUD int, \
    Brand varchar(255), \
    Series varchar(255), \
    ModelNumber varchar(255) \
    HDDCapacity int, \
    HDDPricePerTB int"
    , "CPU": "" # TODO: Create CPU schema
    , "GPU": "" # TODO: Create GPU schema
}


### Functions
# TODO:
# Seperate logic and functions by file:
# scrape.py
# extract_functions.py
# sql_functions.py

def extract_pccg(soup, data_type):
    data = []
    for product in soup.find_all('div', class_="product-container"):
        
        ### Common attributes
        # Data extracted from DOM
        p_title = product.find_next("a", class_="product-title").string
        p_url = product.find_next("a", class_="product-title").attrs["href"]
        # p_incomplete_desc = product.find_next("p").string
        p_price_aud = int(product.find_next("div", class_="price").string.strip("$")) # "$123" --> 123

        # Data extrapolated from previous extraction
        p_title_array = p_title.split()
        # p_incomplete_desc_array = p_incomplete_desc.split()
        p_hdd_capacity = int(next(x for x in p_title_array if x.__contains__("TB")).strip("TB")) # "10TB" --> 10
        p_hdd_price_per_tb = round(p_price_aud/p_hdd_capacity, 2) # Round to two decimal places


        # Brand/Series/Model fuckery, extrapolated from Title
        if p_title_array[0] == "Western":
            p_brand = "Western Digital"
            p_series = p_title_array[3] # "Blue"
            if p_series == "Red": # Logic to handle multi-word series names
                p_series += " " + p_title_array[4] # "Red Plus"
                p_model_number = p_title_array[6] # "WD8001FZBX"
            else:
                # p_series is already correct
                p_model_number = p_title_array[5]
        
        elif p_title_array[0] == "Seagate":
            p_brand = "Seagate"
            p_series = p_title_array[1] # "Ironwolf"
            p_model_number = p_title_array[3] # "ST8000VN004"
        
        # TODO:
        # Separate common & unique attribute extraction logic.
        # Eg Title/price/URL are common attributes
        # HDD Capacity is unique

        # match data_type:
        #     case "HDD" or "hdd":
        #         p_hdd_capacity = int(next(x for x in p_title_array if x.__contains__("TB")).strip("TB")) # "10TB" --> 10
        #         p_hdd_price_per_tb = round(p_price_aud/p_hdd_capacity, 2)
        #     case _:
        #         pass

        data.append({
            "Time": time.strftime("%Y-%m-%d %H:%M:%S")
            , "Retailer": "PCCG"
            , "Title": p_title
            , "URL": p_url
            # , "IncompleteDescription": p_incomplete_desc
            , "PriceAUD": p_price_aud
            , "Brand": p_brand
            , "Series": p_series
            , "ModelNumber": p_model_number
            , "HDDCapacity": p_hdd_capacity
            , "HDDPricePerTB": p_hdd_price_per_tb
        })

    # Just sign-posting a lil' bit
    print("Successfully extracted data from PCCG {} webpage".format(data_type))

    return data

def sql_create_database(cnx):
    try:
        cnx.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(SQL_DB))
        cnx.execute("USE {}".format(SQL_DB))
        print("Successfully created & entered database {}".format(SQL_DB))
    except err:
        print("Failed creating database: {}".format(err))
        exit(1)

def sql_drop_tables(cnx):
    try:
        cnx.execute("SET FOREIGN_KEY_CHECKS = 0")
        for i in len(SQL_TABLES):
            table_name = list(SQL_TABLES)[i - 1] # This absolute horror is only to get the dict keys
            cnx.execute("DROP TABLE IF EXISTS {}".format(table_name))
            print("Successfully dropped table {}".format(table_name))
        cnx.execute("SET FOREIGN_KEY_CHECKS = 1")
    except err:
        print("Failed dropping tables: {}".format(err))
        exit(1)

def sql_create_table(cnx, name):
    try:
        cnx.execute("CREATE TABLE {} ({})".format(SQL_TABLES[name])) # Get table schema from dict
    except err:
        print("Failed to create table \"{}\": {}".format(name, err))
        exit(1)

def sql_insert_into_hdd(data):
    # Accepts an array of dicts
    # Each dict is one row
    data_type = "HDD" # AKA. table name

    ### Table Schema
    # "Time DATETIME, \
    # Retailer varchar(255), \
    # Title varchar(255), \
    # URL varchar(255), \
    # PriceAUD int, \
    # Brand varchar(255), \
    # Series varchar(255), \
    # ModelNumber varchar(255) \
    # HDDCapacity int, \
    # HDDPricePerTB int"

    ### Results Array
    # "Time": time.strftime("%Y-%m-%d %H:%M:%S")
    # , "Retailer": "PCCG"
    # , "Title": p_title
    # , "URL": p_url
    # # , "IncompleteDescription": p_incomplete_desc
    # , "PriceAUD": p_price_aud
    # , "Brand": p_brand
    # , "Series": p_series
    # , "ModelNumber": p_model_number
    # , "HDDCapacity": p_hdd_capacity
    # , "HDDPricePerTB": p_hdd_price_per_tb

    try:
        for x in data:
            cnx.execute("INSERT INTO {} VALUES(\
                {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\
            ))".format(data_type 
                , x["Time"]
                , x["Retailer"]
                , x["Title"]
                , x["URL"]
                , x["PriceAUD"]
                , x["Brand"]
                , x["Series"]
                , x["ModelNumber"]
                , x["HDDCapacity"]
                , x["HDDPricePerTB"]
            ))

            print("Successfully inserted data into table {}".format(data_type))

    except err:
        print("Failed to insert data into HDD table: {}".format(err))
        exit(1)

def sql_select_all_from_table(name):
    pass


### VARIABLES
# "header" is not needed, and this one should be Chrome 95 anyway
# header = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
url = "https://www.pccasegear.com/data_type/210_344/hard-drives-ssds/3-5-hard-drives"


### Check arguments
# TODO:
# Allow arguments, eg:
# ./scrape.py {website} {data_type}
# ./scrape.py PCCG HDD

### PREP DRIVER
# Start driver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
# driver.implicitly_wait(1)
driver.get(url)

# Hand content to BS
soup = bs(driver.page_source, "html.parser")


### Insert data into database
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
# TODO:
# Decide whether or not to combine data extraction & database insertion

# Create connection
# TODO:
# Seperate into sql_connect() function
try:
    cnx = connector.connect(
        host="localhost"
        , user=SQL_USER
        , password=SQL_PASS
        , database=SQL_DB
    )
except err:
    if err.errno == err.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == err.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()

# Create database
# This function is ok to repeat on each execution, as it contains "IF NOT EXISTS"
sql_create_database(cnx)

# Drop all tables
# TODO:
# Make this conditional
sql_drop_tables(cnx)

# Create HDD table
sql_create_table(cnx, "HDD")

# Extract & insert data into table
sql_insert_into_hdd(extract_pccg(soup, "HDD"))


### PRINT DATA
sql_select_all_from_table("HDD")

