#!/usr/bin/python3

### Imports
from logging import error
import time
from typing import Dict
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

import mysql.connector
# import mysql.connector.errors as err
from mysql.connector import errorcode


### File Imports
import funcs_general
import funcs_extract
import funcs_sql
from script.funcs_extract import extract_pccg
from script.funcs_sql import sql_create_database, sql_create_tables, sql_insert_into_hdd, sql_select_all_from_table


### Globals
global SQL_HOST, SQL_USER, SQL_PASS, SQL_DB, SQL_TABLE_NAMES, SQL_TABLE_SCHEMAS
SQL_HOST = "localhost"
# SQL_HOST = "10.1.1.160"
SQL_USER = "scraper"
SQL_PASS = "Password##123"
SQL_DB = "PriceScraper"
SQL_TABLE_NAMES = ["HDD", "SSD", "CPU", "GPU"] # AKA. data types/categories
SQL_TABLE_SCHEMAS = {
    "HDD":
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
    , "SSD":
        "Time DATETIME\
        , Retailer varchar(255)\
        , Title varchar(255)\
        , URL varchar(255)\
        , PriceAUD int\
        , Brand varchar(255)\
        , Series varchar(255)\
        , ModelNumber varchar(255)\
        , SSDCapacity int\
        , SSDPricePerTB int"
    , "CPU": # TODO: Add unique CPU attributes
        "Time DATETIME\
        , Retailer varchar(255)\
        , Title varchar(255)\
        , URL varchar(255)\
        , PriceAUD int\
        , Brand varchar(255)\
        , Series varchar(255)\
        , ModelNumber varchar(255)"
    , "GPU": # TODO: Add unique GPU attributes
        "Time DATETIME\
        , Retailer varchar(255)\
        , Title varchar(255)\
        , URL varchar(255)\
        , PriceAUD int\
        , Brand varchar(255)\
        , Series varchar(255)\
        , ModelNumber varchar(255)"
}


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
sql_create_tables(cursor)

# Extract & insert data into table
test_data = extract_pccg(soup, 0)
sql_insert_into_hdd(cursor, test_data)


### PRINT DATA
sql_select_all_from_table(0)


### Close SQL connection
cnx.close()

