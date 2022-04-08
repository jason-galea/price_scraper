#!/usr/bin/python3

### Imports
# from logging import error
import os
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


### Globals
OUT_JSON_DIR = os.path.abspath(os.path.dirname(__file__))
# OUT_JSON_FILE = f"{}/"
print(OUT_JSON_DIR)
exit()

def main():
    # soup = Web.GetPageChrome("PCCG", "HDD")
    soup = Web.GetPage("PCCG", "HDD")

    # Extract & Insert
    test_data = Extract.pccg(soup, "HDD")
    # print(test_data)
    # print(json.dumps(test_data, indent=4))



    return

if __name__ == "__main__":
    main()

