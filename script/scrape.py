#!/usr/bin/python3

### Imports
from logging import error
# import time
from typing import Dict
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs


### File Imports
from Extract import Extract
from SQL import SQL
from Web import Web


### Check arguments
# TODO: Allow arguments, eg:
# $ ./scrape.py {website} {data_type}
# $ ./scrape.py PCCG HDD
# Each execution would extract data & insert into the appropriate table, then close


soup = Web.GetPage("PCCG", "HDD")


### Open connection
MySQL = SQL()

MySQL.use_database()

# TODO: Make this conditional
#MySQL.drop_tables()

MySQL.create_tables()

test_data = Extract.pccg(soup, "HDD")
MySQL.InsertIntoTable.hdd(test_data, MySQL.cnx)

MySQL.select_all_from_table("HDD")

MySQL.close()
exit(0)

