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
from Web import Web


### Globals
NOW = time.strftime("%Y-%m-%d_%H-%M-%S")
WEBSITE = "PCCG"
CATEGORY = "HDD"
OUT_JSON_DIR = f"{os.path.abspath(os.path.dirname(__file__))}/../out"
OUT_JSON_FILE = f"{OUT_JSON_DIR}/{WEBSITE}_{CATEGORY}_{NOW}.json"
# print(OUT_JSON_DIR)
# print(OUT_JSON_FILE)
# print(NOW)
# exit()

def main():
    ### Check arguments
    # TODO: Allow arguments, eg:
    # $ ./scrape.py {website} {data_type}
    # $ ./scrape.py PCCG HDD
    # Each execution would extract data & insert into the appropriate table, then close


    ### Fetch
    # soup = Web.GetPageChrome(WEBSITE, CATEGORY)
    soup = Web.GetPage(WEBSITE, CATEGORY)


    ### Extract
    test_data = Extract.pccg(soup, CATEGORY) # TODO: Modify class to accept "WEBSITE" programmatically
    print(test_data)
    print(json.dumps(test_data, indent=4))
    exit()


    ### Export
    if not os.path.exists(OUT_JSON_DIR):
        os.makedirs(OUT_JSON_DIR)
    f = open(OUT_JSON_FILE, "w")
    f.write(json.dumps(test_data, indent=4))



    return

if __name__ == "__main__":
    main()

