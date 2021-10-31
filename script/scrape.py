#!/usr/bin/python3

### Imports
from logging import error
# import time
from typing import Dict
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

# import mysql.connector
# import mysql.connector.errors as err
# from mysql.connector import errorcode


### File Imports
# from funcs_general import ???
from Extract import Extract
from SQL import SQL



### Variables
# "header" is not needed, and this one should be Chrome 95 anyway
# header = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
url = "https://www.pccasegear.com/category/210_344/hard-drives-ssds/3-5-hard-drives"


### Check arguments
# TODO: Allow arguments, eg:
# ./scrape.py {website} {data_type}
# ./scrape.py PCCG HDD

### PREP DRIVER
# TODO: Separate into function
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


### Create SQL object (which opens the connection)
MySQL = SQL()
print("Success: Connected to MySQL on {}".format(SQL.HOST))

SQL.use_database()

# TODO: Make this conditional
SQL.drop_tables()

SQL.create_tables()

test_data = Extract.pccg(soup, "HDD")
SQL.insert_into_hdd(test_data)

SQL.select_all_from_table("HDD")

SQL.close()

