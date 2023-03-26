#!/usr/bin/env python3

import os
import json
import datetime
import html
import threading
import pandas as pd
from glob import glob
from flask import Flask, render_template, request
from selenium.common.exceptions import WebDriverException

# import lib.Extract as Extract
from lib.PCCG import PCCG
from lib.Scorptec import Scorptec
from lib.CentreCom import CentreCom


###########################################################
### GLOBAL VARS
app = Flask(__name__)
ROOT = app.root_path

CONF_DIR = f"{ROOT}/conf"
JSON_OUTPUT_DIR = f"{ROOT}/out"

with open(f"{CONF_DIR}/page_info.json", "r") as f: PAGE_INFO = json.load(f)
with open(f"{CONF_DIR}/form_labels.json", "r") as f: FORM_LABELS = json.load(f)
with open(f"{CONF_DIR}/table_cols.json", "r") as f: TABLE_COLS = json.load(f)

FORM_COLS = ['website', 'category']


###########################################################
### Generic functions
def get_json_filenames() -> list:
    return glob(f"{JSON_OUTPUT_DIR}/*.json")

def listContainsAllValues(haystack, needles) -> list:
    return all((n in haystack) for n in needles)


###########################################################
### Route-specific functions
def scrape_start_extract_thread(website, category) -> None:

    ### TODO: Check if another thread is already running
    # if (???):
    #     print(f"\n==> ERROR: Another thread is already running, please wait a moment for it to finish")
    #     return

    NOW = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    JSON_OUTPUT_FILE = f"{JSON_OUTPUT_DIR}/{NOW}_{website}_{category}.json"

    match website:
        case "pccg": website_class = PCCG
        case "scorptec": website_class = Scorptec
        case "centrecom": website_class = CentreCom

    # print(f"\n==> INFO: Scraping with website '{website}' and category '{category}'")
    scrape_thread = threading.Thread(
        target=website_class,
        args=(category, JSON_OUTPUT_DIR, JSON_OUTPUT_FILE),
    )

    print(f"\n==> INFO: Launching thread to scrape '{category}' data from '{website}'")
    scrape_thread.start()
    # while True:
    #     try:
    #         scrape_thread.start()
    #         break
    #     except WebDriverException as e:
    #         print(f"\n==> WARN: WebDriverException exception raised: '{e}'")
    #         print(f"\n==> WARN: This was most likely caused by conflicting threads")
    #         print(f"\n==> WARN: Restarting thread")
    #         continue


def table_get_template_vars(website, category) -> dict:

    ### Filter to files containing the chosen website & category
    filtered_files = [ item
        for item in get_json_filenames()
        if (listContainsAllValues(item.split('.')[0].split("_"), [website, category]))
    ]
    # print(f"filtered_files = {filtered_files}")
    latest_file = max(filtered_files, key=os.path.getctime)
    latest_file_basename = os.path.basename(latest_file)

    ### DEBUG
    # print(f"latest_file = {latest_file}")
    # print(f"latest_file_basename = {latest_file_basename}")

    ### Read
    df = pd.read_json(latest_file)

    ### Clean up Title col
    df['Title'] = df.apply(table_fix_title_col, axis=1)

    ### Create col with embedded URL
    df['TitleLink'] = df.apply(
        lambda row: f"<a href={row['URL']}>{row['Title']}</a>",
        axis=1,
    )

    ### Restrict & sort cols
    df = df[TABLE_COLS[category]['display_cols']]
    df = df.sort_values(TABLE_COLS[category]['sort_col'], ignore_index=True)

    ### Escape all cols except "TitleLink"
    df[[
        c
        for c in list(df.columns)
        if (c != 'TitleLink')
    ]].apply( html.escape, axis=1 )

    return {
        # 'latest_file': latest_file,
        'latest_file_basename': latest_file_basename, ### Signposting
        'table_html': df.to_html(escape=False)
    }

def table_fix_title_col(row) -> str:
    match_replace_dict = {
        'Hard Drive': 'HDD',
        '3.5in ': '',
        'WD ': '',
    }
    result = str(row["Title"])
    
    for match, replace in match_replace_dict.items():
        result = result.replace(match, replace)

    return result


###########################################################
### Flask routes
@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def routes(path='index'):

    # key = path ### Deal with it
    common_vars = {
        'PAGE_INFO': PAGE_INFO,
        'key': path,
        'template_name_or_list': PAGE_INFO[path]['template'],
        'desc': PAGE_INFO[path]['desc'],
    }
    page_vars = {
        "FORM_LABELS": FORM_LABELS,
        **request.form,
    }

    FORM_IS_VALID = listContainsAllValues(page_vars.keys(), FORM_COLS)
    if FORM_IS_VALID:
        website = page_vars['website']
        category = page_vars['category']

    match path:
        case "index":
            pass

        case "scrape":
            if FORM_IS_VALID:
                scrape_start_extract_thread(website, category)

        case "table":
            if FORM_IS_VALID:
                page_vars.update( table_get_template_vars(website, category) )

        case "graph":
            pass

        case "results":
            results = [os.path.basename(s) for s in get_json_filenames()]
            results.sort(reverse=True) ### Sort by reverse date, newest items on top

            page_vars.update({ 'results': results })


    ### DEBUG
    # print(f"\npage_vars: \n{json.dumps(page_vars, indent=2)}\n")


    ###########################################################
    ### Render
    return render_template(
        **common_vars,
        **page_vars,
    )


if __name__ == '__main__':
    app.run(
        # debug=True,
        host='0.0.0.0',
    )
