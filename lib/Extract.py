#!/usr/bin/python3

import os
import datetime
import enum
import json

from lib.PCCG import PCCG
from lib.Scorptec import Scorptec
from lib.CentreCom import CentreCom


# def export_json(extracted_data, dir, file):
#     print(f"\nExporting data to {file}\n")

#     ### Check/Create dir
#     if not os.path.exists(dir):
#         os.makedirs(dir)

#     ### Write
#     with open(file, "w") as f:
#         f.write(json.dumps(extracted_data))

# def entrypoint(website, category, output_dir, debug=False):
#     NOW = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S') 
#     # OUT_JSON_DIR = f"{os.path.abspath(os.path.dirname(__file__))}/../out" ### This shit sucks
#     OUT_JSON_FILE = f"{output_dir}/{NOW}_{website}_{category}.json"

#     match website:
#         case "pccg":
#             my_extract_instance = PCCG(category)
#         case "scorptec":
#             my_extract_instance = Scorptec(category)
#         case "centrecom":
#             my_extract_instance = CentreCom(category)


#     ########################################################################
#     ### NOTE: Actually, there's no point returning these values here.
#     ### NOTE: Keeping this logic within each class makes more sense
#     ### NOTE: Moving this into "__init__" would allow for unique logic
#     ########################################################################


#     ### Download HTML
#     bs4_html_parser = my_extract_instance.download_html()

#     ### Extract
#     extracted_data = my_extract_instance.extract(bs4_html_parser)

#     ### Debug
#     if (debug):
#         print(json.dumps(extracted_data, indent=4))

#     ### Export
#     export_json(extracted_data, output_dir, OUT_JSON_FILE)

#     ### Cleanup
#     os.system('pkill firefox') ### Lol. Lmao
#     return ### TODO: Delete this, right? 


# def entrypoint(website, category, output_dir, debug=False):
def entrypoint(website, category, output_dir):
    NOW = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S') 
    # OUT_JSON_DIR = f"{os.path.abspath(os.path.dirname(__file__))}/../out" ### This shit sucks
    OUT_JSON_FILE = f"{output_dir}/{NOW}_{website}_{category}.json"

    match website:
        case "pccg":
            PCCG(category, output_dir, OUT_JSON_FILE)
        case "scorptec":
            Scorptec(category, output_dir, OUT_JSON_FILE)
        case "centrecom":
            CentreCom(category, output_dir, OUT_JSON_FILE)
