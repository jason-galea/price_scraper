#!/usr/bin/python3

### Imports
# from logging import error
import time
import json
# from typing import Dict
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup as bs


### File Imports
from Extract import Extract
from SQL import SQL
from Web import Web


### Check arguments
# TODO: Allow arguments, eg:
# $ ./scrape.py {website} {data_type}
# $ ./scrape.py PCCG HDD
# Each execution would extract data & insert into the appropriate table, then close

def main():
    # soup = Web.GetPageChrome("PCCG", "HDD")
    soup = Web.GetPageFirefox("PCCG", "HDD")

    # Extract & Insert
    test_data = Extract.pccg(soup, "HDD")
    # print(test_data)
    print(json.dumps(test_data, indent=4))

    ### Open SQL
    # MySQL = SQL()
    # MySQL.use_database()
    # MySQL.create_tables() # Don't overwrite existing tables

    ### Insert
    # MySQL.Insert.hdd(test_data, MySQL.cnx)

    ### Close SQL
    # MySQL.select_all_from_table("HDD")
    # MySQL.close()


    return

if __name__ == "__main__":
    main()

