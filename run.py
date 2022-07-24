#!/usr/bin/python3

### Imports
import os
import json
import html
from posixpath import basename
import subprocess as sp
from unicodedata import category
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

ROOT = app.root_path
OUT_DIR = f"{ROOT}/out"
FORM_COLS = ['website', 'category']


###########################################################
### Generic functions
def readForm(request_values):
    
    ### Create
    result = { 'FORM_LABELS':FORM_LABELS }

    ### Get form vars (if they exist)
    for s in FORM_COLS:
        val = request_values.get(s)
        if (val != None):
            result.update({ s:val })

    return result

def readAllJSON():
    return glob(f"{OUT_DIR}/*.json")

def getHaystackMatchingNeedles(needles, haystack):
    ### TODO: Refactor to only account for web and cat
    result = []

    for item in haystack:
        # tokens = os.path.splitext(item)[0].split("_")
        tokens = item.split('.')[0].split("_")

        flag = False
        for needle in needles:
            if not needle in tokens:
                flag = True
                break
        
        if not flag:
            result.append(item)
    
    return result

def listContainsAllValues(haystack, needles):
    return not any((n not in haystack) for n in needles)

###########################################################
### Route-specific functions
def scrape_StartSubprocess(unique_context):
    cmd = f"{ROOT}/script/scrape.py {unique_context['website']} {unique_context['category']}"
    # _p = sp.Popen(cmd.split())
    sp.Popen(cmd.split())

def viewTable_GetVars(unique_context):

    ### Filter to files containing the chosen website & category
    needles = [unique_context['website'], unique_context['category']]
    # filtered_files = getHaystackMatchingNeedles(needles, readAllJSON())
    filtered_files = [
        s for s in readAllJSON()
        if listContainsAllValues(s.split('.')[0].split("_"), needles)
    ]
    latest_file = max(filtered_files, key=os.path.getctime)

    df = pd.read_json(latest_file)

    ### Create col with embedded URL
    df['TitleLink'] = df.apply(
        lambda row: f"<a href={row['URL']}>{row['Title']}</a>",
        axis=1,
    )

    ### Restrict columns
    df = df[['Retailer', 'TitleLink', 'Brand', 'PriceAUD', 'CapacityTB', 'PricePerTB']]
    df = df.sort_values('PricePerTB', ignore_index=True)

    ### Escape all cols (except TitleLink)
    df[[c for c in list(df.columns) if (c != 'TitleLink')]].apply( html.escape, axis=1 )

    return {
        'latest_file': latest_file,
        'table_html': df.to_html(escape=False)
    }


###########################################################
### Flask routes
### TODO: Explode this function into separate pages (and combine after logic complete?)
@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def routes(path='index'):

    key = path ### Deal with it
    unique_context = {}


    ###########################################################
    ### Get form vars
    if (key in ['scrape', 'table', 'graph']):
        unique_context = readForm(request.values)


    ###########################################################
    ### Get unique vars
    ### No switch-case in python 3.9, kill me
    if (key == 'index'):
        pass
        # print()
        # print(f"os.path.dirname(app.root_path) = {os.path.dirname(app.root_path)}")
        # print(f"os.path.dirname(app.instance_path) = {os.path.dirname(app.instance_path)}")
        # print(f"app.root_path = {app.root_path}")
        # print(f"app.instance_path = {app.instance_path}")
        # print()

    elif (key == 'scrape'):
        if listContainsAllValues(unique_context.keys(), FORM_COLS):
            scrape_StartSubprocess(unique_context)

    elif (key == 'table'):
        if listContainsAllValues(unique_context.keys(), FORM_COLS):
            unique_context.update( viewTable_GetVars(unique_context) )

    elif (key == 'graph'):
        pass

    elif (key == 'results'):
        unique_context.update({ 'results': readAllJSON() })


    ###########################################################
    ### Render
    # print(f"\nunique_context: \n{json.dumps(unique_context, indent=2)}\n")
    return render_template(
        template_name_or_list= PAGE_INFO[key]['template'],
        key= key,
        PAGE_INFO= PAGE_INFO,
        desc= PAGE_INFO[key]['desc'],
        **unique_context,
    )

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
    )
