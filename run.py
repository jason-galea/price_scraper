#!/usr/bin/python3

### Imports
import os
import json
import html
import subprocess as sp
import pandas as pd

# from multiprocessing import context
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    flash,
    redirect,
)
from glob import glob




###########################################################
### Vars
app = Flask(__name__)

PAGE_INFO = {
    'index':{
        'route':'/',
        'template':'children/index.html',
        'title':'Home',
        'desc':[
            'Welcome to Price Scraper (TM)!',
            'This website will scrape & display the latest price/specs/etc. of computer hardware.',
            'It\'s designed to work with specific Australian computer parts retailers.',
        ],
    },
    'scrape':{
        'route':'/scrape',
        'template':'children/scrape.html',
        'title':'Scrape',
        'desc':[
            'This page lets you scrape the latest data from your chosen website & category.',
            'Make a selection and press "Submit" to continue.',
        ],
    },
    'table':{
        'route':'/table',
        'template':'children/table.html',
        'title':'Table',
        'desc':[
            'This page allows you to view the most recent result for a given website & category.',
            'The data will be displayed in a table.',
            'Make a selection and press "Submit" to continue.',
        ],
    },
    'graph':{
        'route':'/graph',
        'template':'children/graph.html',
        'title':'Graph',
        'desc':[
            'This page allows you to view the most recent result for a given website & category.',
            'The data will be displayed in a graph.',
            'Make a selection and press "Submit" to continue.',
        ],
    },
    'results':{
        'route':'/results',
        'template':'children/results.html',
        'title':'Results',
        'desc':[
            'This page shows all previously collected result files.',
            'In case of any error, collecting some more data in the "Scrape" page',
        ],
    },
    # '':{
    #     'route':'',
    #     'template':'',
    #     'title':'',
    #     'desc':'',
    # },
}

FORM_LABELS = {
    'website':{
        'pccg':'PC Case Gear',
        'scorptec':'Scorptec',
        'centrecom':'Centre Com',
    },
    'category':{
        'hdd':'3.5\' Hard Drive',
        'ssd':'SSD',
        'cpu':'CPU',
        'gpu':'GPU',
    },
}

TABLE_COLS = {
    'hdd':{
        'display_cols': ['Retailer', 'TitleLink', 'Brand', 'PriceAUD', 
            'CapacityGB', 'CapacityTB', 'PricePerTB'],
        'sort_col':'PricePerTB',
    },
    'ssd':{
        'display_cols': ['Retailer', 'TitleLink', 'Brand', 'PriceAUD',
            'CapacityGB', 'CapacityTB', 'PricePerTB'],
        'sort_col':'PricePerTB',
    },
    # 'cpu':{
    #     'display_cols':['Retailer', 'TitleLink', 'Brand', 'PriceAUD', 'CapacityTB', 'PricePerTB'],
    #     'sort_col':'PricePerTB',
    # },
    # 'gpu':{
    #     'display_cols':['Retailer', 'TitleLink', 'Brand', 'PriceAUD', 'CapacityTB', 'PricePerTB'],
    #     'sort_col':'PricePerTB',
    # },
}

ROOT = app.root_path
JSON_OUTPUT_DIR = os.path.join(ROOT, "out")
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
    return glob(os.path.join(JSON_OUTPUT_DIR, "*.json"))

# def getMatchingFiles(haystack, needles):
#     return [item for item in haystack if (listContainsAllValues(item.split('.')[0].split("_"), needles))]

def listContainsAllValues(haystack, needles):
    return all((n in haystack) for n in needles)


###########################################################
### Route-specific functions
def scrape_StartSubprocess(page_vars):
    cmd = f"{ROOT}/script/scrape.py {page_vars['website']} {page_vars['category']}"

    sp.Popen(cmd.split())

def viewTable_GetVars(page_vars):

    ### Vars
    website = page_vars['website']
    category = page_vars['category']

    ### Filter to files containing the chosen website & category
    filtered_files = [ item
        for item in getJSONFilenames()
        if (listContainsAllValues(item.split('.')[0].split("_"), [website, category]))
    ]

    # print(f"\nROOT = {ROOT}\n")
    # print(f"\nJSON_OUTPUT_DIR = {JSON_OUTPUT_DIR}\n")
    # print(f"\nmax(filtered_files, key=os.path.getctime) = {max(filtered_files, key=os.path.getctime)}\n")
    # latest_file = f"{JSON_OUTPUT_DIR}/{max(filtered_files, key=os.path.getctime)}"
    latest_file = os.path.join(JSON_OUTPUT_DIR, max(filtered_files, key=os.path.getctime))

    ### DEBUG
    print(f"\nlatest_file = {latest_file}\n")

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
        'latest_file_short': os.path.basename(latest_file), ### Signposting
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
                scrape_StartSubprocess(page_vars)

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


    ###########################################################
    ### DEBUG
    print(f"\npage_vars: \n{json.dumps(page_vars, indent=2)}\n")
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
