#!/usr/bin/python3

import os
from os import path
import sys
import datetime
import json

from Extract import Extract 
from Web import Web


### FUNCTIONS
def export(test_data, dir, file):
    print(f"\nExporting data to {file}\n")

    # Check/Create dir
    if not path.exists(dir):
        os.makedirs(dir)

    # Write
    f = open(file, 'w')
    # f.write(json.dumps(test_data, indent=4)) # The indents definitely don't need to be here
    f.write(json.dumps(test_data))


### MAIN
def main():

    ### Require args
    if (len(sys.argv) in [1, 2]):
        print('\nPlease provide website & category as arguments, E.G:')
        print('$ scrape.py pccg hdd\n')
        print('$ scrape.py scorptec gpu --debug\n')
        exit(1)
        

    ### Vars
    DEBUG = ('--debug' in sys.argv)
    NOW = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S') 
    WEBSITE = sys.argv[1] # 'pccg'
    CATEGORY = sys.argv[2] # 'hdd'
    OUT_JSON_DIR = f"{path.abspath(path.dirname(__file__))}/../out"
    OUT_JSON_FILE = f"{OUT_JSON_DIR}/{NOW}_{WEBSITE}_{CATEGORY}.json"
    
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
    URL = URLS[WEBSITE][CATEGORY]

    ### Begin
    soup = Web.GetPageSoup(URL)
    test_data = Extract.extract(WEBSITE, CATEGORY, soup)

    ### Debug
    if (DEBUG):
        # print(test_data)
        print(json.dumps(test_data, indent=4))
        # exit()


    ### Export
    export(test_data, OUT_JSON_DIR, OUT_JSON_FILE)


    ### Cleanup
    os.system('pkill firefox')
    return

if __name__ == '__main__':
    main()

