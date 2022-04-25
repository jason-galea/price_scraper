#!/usr/bin/python3


### IMPORTS
import os
from os import path
import datetime
import json

from Extract import Extract 
from Web import Web
# import Extract # AttributeError: module 'Web' has no attribute 'GetPage'
# import Web


### FUNCTIONS
def export(test_data, dir, file):
    print(f"\nExporting data to {file}\n")

    # Check/Create dir
    if not path.exists(dir):
        os.makedirs(dir)

    # Write
    f = open(file, "w")
    # f.write(json.dumps(test_data, indent=4)) # The indents definitely don't need to be here
    f.write(json.dumps(test_data))


### MAIN
def main():

    ### Check arguments
    # TODO: Allow arguments, eg:
    # $ ./scrape.py {website} {data_type}
    # $ ./scrape.py PCCG HDD


    ### Vars
    NOW = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S") # UTC is much easier
    WEBSITE = "PCCG"
    CATEGORY = "HDD"
    # OUT_JSON_DIR = f"{path.abspath(path.dirname(__file__))}/../scrape_result"
    OUT_JSON_DIR = f"{path.abspath(path.dirname(__file__))}/../out"
    OUT_JSON_FILE = f"{OUT_JSON_DIR}/scrape_result_{WEBSITE}_{CATEGORY}_{NOW}.json"


    ### Fetch
    soup = Web.GetPage(WEBSITE, CATEGORY)


    ### Extract
    test_data = Extract.pccg(soup, CATEGORY) # TODO: Modify class to accept "WEBSITE" programmatically
    # print(test_data)
    print(json.dumps(test_data, indent=4))
    # exit()


    ### Export
    # print(f"\nExporting data to {OUT_JSON_FILE}\n")
    # if not path.exists(OUT_JSON_DIR):
    #     os.makedirs(OUT_JSON_DIR)
    # f = open(OUT_JSON_FILE, "w")
    # # f.write(json.dumps(test_data, indent=4)) # The indents definitely don't need to be here
    # f.write(json.dumps(test_data))
    export(test_data, OUT_JSON_DIR, OUT_JSON_FILE)


    ### Cleanup
    os.system("pkill firefox")
    return

if __name__ == "__main__":
    main()

