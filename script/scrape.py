#!/usr/bin/python3

### Imports
import os
import time
import json

from Extract import Extract
from Web import Web


def main():
    ### Vars        
    NOW = time.strftime("%Y-%m-%d_%H-%M-%S")
    WEBSITE = "PCCG"
    CATEGORY = "HDD"
    # OUT_JSON_DIR = f"{os.path.abspath(os.path.dirname(__file__))}/../scrape_result"
    OUT_JSON_DIR = f"{os.path.abspath(os.path.dirname(__file__))}/../out"
    OUT_JSON_FILE = f"{OUT_JSON_DIR}/scrape_result_{WEBSITE}_{CATEGORY}_{NOW}.json"
    # OUT_JSON_FILE = f"{OUT_JSON_DIR}/out_{WEBSITE}_{CATEGORY}_{NOW}.json"
    # print(OUT_JSON_DIR)
    # print(OUT_JSON_FILE)
    # print(NOW)
    # exit()

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
    # print(test_data)
    print(json.dumps(test_data, indent=4))
    # exit()


    ### Export
    print(f"\nExporting data to {OUT_JSON_FILE}")
    if not os.path.exists(OUT_JSON_DIR):
        os.makedirs(OUT_JSON_DIR)
    f = open(OUT_JSON_FILE, "w")
    # f.write(json.dumps(test_data, indent=4)) # The indents definitely don't need to be here
    f.write(json.dumps(test_data))



    return

if __name__ == "__main__":
    main()

