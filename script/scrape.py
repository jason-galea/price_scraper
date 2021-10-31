#!/usr/bin/python3

### Imports
import time
from typing import Dict
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

import mysql.connector
import mysql.connector.errors as err
from mysql.connector import errorcode


### Constants
SQL_HOST = "localhost"
# SQL_HOST = "10.1.1.160"
SQL_USER = "scraper"
SQL_PASS = "Password##123"
SQL_DB = "PriceScraper"
SQL_TABLE_NAMES = ["HDD", "SSD", "CPU", "GPU"] # AKA. data types/categories
SQL_TABLE_SCHEMAS = [
    "Time DATETIME\
    , Retailer varchar(255)\
    , Title varchar(255)\
    , URL varchar(255)\
    , PriceAUD int\
    , Brand varchar(255)\
    , Series varchar(255)\
    , ModelNumber varchar(255)\
    , HDDCapacity int\
    , HDDPricePerTB int"
    , "" # TODO: Create SSD schema
    , "" # TODO: Create CPU schema
    , "" # TODO: Create GPU schema
]


### Functions
# TODO: Seperate logic and functions by file:
# scrape.py
# extract_functions.py
# sql_functions.py

def extract_pccg(soup, table_index):
    data = []
    data_type = SQL_TABLE_NAMES[table_index]

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
        
        # TODO: Separate common & unique attribute extraction logic.
        # Eg Title/price/URL are common attributes
        # HDD Capacity is unique

        # match data_type:
        #     case "HDD":
        #         p_hdd_capacity = int(next(x for x in p_title_array if x.__contains__("TB")).strip("TB")) # "10TB" --> 10
        #         p_hdd_price_per_tb = round(p_price_aud/p_hdd_capacity, 2)
        #     case _: # Default case
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
    print("Success: Extracted data from PCCG {} webpage".format(data_type))
    # print()
    # print(data)
    # print()

    return data

def sql_create_database(cursor):
    try:
        # No need for "IF NOT EXISTS", because this function is only called to OVERWRITE a corrupt DB? I think?
        # cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(SQL_DB))
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(SQL_DB))
        print("Success: Created database {}".format(SQL_DB))
    except err:
        print("Failure: Could not create database: \n{}".format(err.msg))
        exit(1)

def sql_drop_tables(cursor):
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        for name in SQL_TABLE_NAMES:
            cursor.execute("DROP TABLE IF EXISTS {}".format(name))
            print("Success: Dropped table {}".format(name)) # Will "succeed" even if table was already dropped.

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    except err:
        print("Failure: Could not drop tables: \n{}".format(err.msg))
        exit(1)

def sql_create_table(cursor, table_index):
    try:
        cursor.execute("CREATE TABLE {} ({})".format(SQL_TABLE_NAMES[table_index], SQL_TABLE_SCHEMAS[table_index]))
        print("Success: Created table {}".format(SQL_TABLE_NAMES[table_index]))
    except err:
        print("Failure: Could not create table {}: \n{}".format(SQL_TABLE_NAMES[table_index], err.msg))
        exit(1)

def sql_insert_into_hdd(data):
    # Accepts an array of dicts
    # Each dict is one row
    data_type = "HDD" # AKA. table name

    try:
        for x in data:
            cursor.execute("INSERT INTO '{}' VALUES(\
                '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'\
            )".format(data_type 
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

            print("Success: Inserted data into table {}".format(data_type))

    except err:
        print("Failure: Could not insert data into table {}: \n{}".format(data_type, err.msg))
        exit(1)

def sql_select_all_from_table(table_index):
    name = SQL_TABLE_NAMES[table_index]
    pass


### VARIABLES
# "header" is not needed, and this one should be Chrome 95 anyway
# header = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
url = "https://www.pccasegear.com/category/210_344/hard-drives-ssds/3-5-hard-drives"


### Check arguments
# TODO: Allow arguments, eg:
# ./scrape.py {website} {data_type}
# ./scrape.py PCCG HDD

### PREP DRIVER
# TODO: Separate into function
# Start driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--headless')
# https://stackoverflow.com/questions/53902507/unknown-error-session-deleted-because-of-page-crash-from-unknown-error-cannot
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)
# driver.implicitly_wait(1)
driver.get(url)

# Hand page content to BS
soup = bs(driver.page_source, "html.parser")



### https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
# Create connection
cnx = mysql.connector.connect(
    host=SQL_HOST
    , user=SQL_USER
    , password=SQL_PASS
    , database=SQL_DB
)
cursor = cnx.cursor()
print("Success: Connected to MySQL on {}".format(SQL_HOST))


# Use/create database
try:
    cursor.execute("USE {}".format(SQL_DB))
    # cnx.database = SQL_DB
except mysql.connector.Error as err:
    print("Failure: Database {} does not exist".format(SQL_DB))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        sql_create_database(cursor)
        print("Success: Database {} created".format(SQL_DB))
        # cursor.execute("USE {}".format(SQL_DB))
        cnx.database = SQL_DB
    else:
        print(err.msg) # This error would be non-specific, so I can't describe it beforehand
        exit(1)
print("Success: Now using database {}".format(SQL_DB))

# Drop all tables
# TODO: Make this conditional
# sql_drop_tables(cursor)

# Create tables
# TODO: Make this a loop, when the schemas for other tables are complete
sql_create_table(cursor, 0)

# Extract & insert data into table
test_data = extract_pccg(soup, 0)
sql_insert_into_hdd(test_data)


### PRINT DATA
sql_select_all_from_table(0)


### Close SQL connection
cnx.close()

