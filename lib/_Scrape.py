#!/usr/bin/python3

import os
from os import path
import sys
import datetime
import json

import lib.Extract as Extract
import lib._Web as _Web
# from lib.Extract import Extract
# from lib.Web import Web


### GLOBALS
URLS = {
    'pccg': {
        'hdd': 'https://www.pccasegear.com/category/210_344/hard-drives-ssds/3-5-hard-drives',
        'ssd': 'https://www.pccasegear.com/category/210_902/hard-drives-ssds/solid-state-drives-ssd',
        'cpu': '',
        'gpu': '',
    },
    'scorptec': {
        'hdd': '',
        'ssd': '',
        'cpu': '',
        'gpu': '',
    },
    # etc...
}

### MAIN
def Scrape(website, category, debug=False):

    ### Vars
    NOW = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S') 
    OUT_JSON_DIR = f"{path.abspath(path.dirname(__file__))}/../out"
    OUT_JSON_FILE = f"{OUT_JSON_DIR}/{NOW}_{website}_{category}.json"
    URL = URLS[website][category]

    ### Begin
    Extract.entrypoint(website, category, OUT_JSON_DIR, OUT_JSON_DIR)

    ### Download HTML
    # soup = Web.get_BS4_HTML_from_URL(URL)

    ### Extract
    # match website:
    #     case "pccg": extracted_data = Extract.pccg(category, soup)
    #     case "scorptec": extracted_data = Extract.scorptec(category, soup)
    #     case "centrecom": extracted_data = Extract.centrecom(category, soup)
    # extracted_data = Extract.PCCG.begin()


    # ### Debug
    # if (debug):
    #     print(json.dumps(extracted_data, indent=4))

    # ### Export
    # export_to_JSON(extracted_data, OUT_JSON_DIR, OUT_JSON_FILE)

    # ### Cleanup
    # os.system('pkill firefox')
    # return
