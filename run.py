#!/usr/bin/python3

### Imports
import os
import json
import html
# import subprocess as sp
import threading
import pandas as pd

from glob import glob
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    flash,
    redirect,
)
from lib.Scrape import Scrape




###########################################################
### Vars
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
def getFormVars(request_values):
    
    ### Create
    result = {}

    ### Get form vars (if they exist)
    for s in FORM_COLS:
        val = request_values.get(s)
        if (val != None):
            result.update({ s:val })

    return result

def getJSONFilenames():
    return glob(f"{JSON_OUTPUT_DIR}/*.json")

# def getMatchingFiles(haystack, needles):
#     return [item for item in haystack if (listContainsAllValues(item.split('.')[0].split("_"), needles))]

def listContainsAllValues(haystack, needles):
    return all((n in haystack) for n in needles)


###########################################################
### Route-specific functions
def scrape_StartSubprocess(website, category):
    # cmd = f"{ROOT}/script/scrape.py {website} {category}"
    # sp.Popen(cmd.split())

    scrape_thread = threading.Thread(
        target=Scrape,
        args=(website, category),
    )
    scrape_thread.start()

def viewTable_GetVars(page_vars):

    ### Vars
    website = page_vars['website']
    category = page_vars['category']

    ### Filter to files containing the chosen website & category
    filtered_files = [ item
        for item in getJSONFilenames()
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
    df['Title'] = df.apply(viewTable_fixTitleCol, axis=1)

    ### Create col with embedded URL
    df['TitleLink'] = df.apply(
        lambda row: f"<a href={row['URL']}>{row['Title']}</a>",
        axis=1,
    )

    ### Restrict & sort cols
    df = df[TABLE_COLS[category]['display_cols']]
    df = df.sort_values(TABLE_COLS[category]['sort_col'], ignore_index=True)

    ### Escape all cols (except TitleLink)
    df[[c for c in list(df.columns) if (c != 'TitleLink')]].apply( html.escape, axis=1 )

    return {
        # 'latest_file': latest_file,
        'latest_file_basename': latest_file_basename, ### Signposting
        'table_html': df.to_html(escape=False)
    }

def viewTable_fixTitleCol(row):
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
    page_vars = {}

    match path:
        case "index":
            pass

        case "scrape":
            page_vars.update({ 'FORM_LABELS':FORM_LABELS })
            page_vars.update( getFormVars(request.values) )

            if listContainsAllValues(page_vars.keys(), FORM_COLS):
                # scrape_StartSubprocess(page_vars)
                # Scrape(page_vars['website'], page_vars['category'])
                scrape_StartSubprocess(page_vars['website'], page_vars['category'])

        case "table":
            page_vars.update({ 'FORM_LABELS':FORM_LABELS })
            page_vars.update( getFormVars(request.values) )

            if listContainsAllValues(page_vars.keys(), FORM_COLS):
                page_vars.update( viewTable_GetVars(page_vars) )

        case "graph":
            page_vars.update({ 'FORM_LABELS':FORM_LABELS })
            page_vars.update( getFormVars(request.values) )

        case "results":
            results = [os.path.basename(s) for s in getJSONFilenames()] ### 
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
        debug=True,
        host='0.0.0.0',
    )
