#!/usr/bin/python3

### Imports
import subprocess as sp
from multiprocessing import context
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    flash,
    redirect,
)



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
    'view_table':{
        'route':'/view_table',
        'template':'children/view_table.html',
        'title':'Table',
        'desc':[
            'This page allows you to view the most recent result for a given website & category.',
            'The data will be displayed in a table.',
            'Make a selection and press "Submit" to continue.',
        ],
    },
    'view_graph':{
        'route':'/view_graph',
        'template':'children/view_graph.html',
        'title':'Graph',
        'desc':[
            'This page allows you to view the most recent result for a given website & category.',
            'The data will be displayed in a graph.',
            'Make a selection and press "Submit" to continue.',
        ],
    },
    'view_all_results':{
        'route':'/view_all_results',
        'template':'children/view_all_results.html',
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



###########################################################
### Generic functions
def getFormContext(request_values):
    
    ### Create
    result = { 'FORM_LABELS':FORM_LABELS }

    ### Get form vars (if they exist)
    for s in ['website', 'category']:
        val = request_values.get(s)
        if (val != None):
            result.update({ s:val })

    return result

def renderTemplateWithContext(key, unique_context={}):
    ### Create common context args
    context = {
        'key':key,
        'PAGE_INFO':PAGE_INFO,
        'desc':PAGE_INFO[key]['desc'],
    }

    ### Append args unique to the page being rendered
    context.update(unique_context) ### For example, 'website' and 'category'

    ### Render
    return render_template(
        template_name_or_list=PAGE_INFO[key]['template'],
        **context,
    )

def allListItemsExistInList(needle_list, haystack_list):
    ### Returns True if all items in 'needle_list' exist in 'haystack_list'
    ### 'haystack_list' can also be a dict, where 'haystack_list.keys()' will be searched instead

    return (
        all ((k in haystack_list) for k in needle_list)
    )

def getAllResultsFiles():
    ### Returns a list of filenames

    # cmd = 'ls -lh ./out/'
    cmd = 'ls ./out/'

    try:
        return sp.check_output( cmd.split(), encoding='utf-8' ).split('\n')
    except sp.CalledProcessError as e:
        return None


###########################################################
### Route-specific functions
def scrape_StartSubprocess(unique_context):
    ### Start subprocess, if required args are defined
    if allListItemsExistInList(['website', 'category'], unique_context):
        # cmd = './script/scrape.py pccg hdd'
        cmd = f"./script/scrape.py {unique_context['website']} {unique_context['category']}"
        
        # p = sp.run(scrape_command.split()) ### Run & block

        p = sp.Popen(cmd.split()) ### Run 
        # p.communicate() ### Wait & print to STDOUT

def viewAllResults_GetVars():
    # try:
    #     return {
    #         'ls_stdout': getAllResultsFiles,
    #         'sp_success': True
    #     }

    # except sp.CalledProcessError as e:
    #     return {
    #         'ls_stdout': [e], ### The template expects a list
    #         'sp_success': False
    #     }

    return { 'ls_stdout': getAllResultsFiles() }


###########################################################
### Flask routes
### TODO: Explode this function into separate pages (and combine after logic complete?)
@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def routes(path='index'):
    key = path ### Deal with it


    ###########################################################
    ### Get form vars
    if (key in ['scrape', 'view_table', 'view_graph']):
        unique_context = getFormContext(request.values)
    else: 
        unique_context = {}


    ###########################################################
    ### Get unique vars
    ### No switch-case in python 3.9, kill me
    if (key == 'index'):
        pass
    elif (key == 'scrape'):
        scrape_StartSubprocess(unique_context)
    elif (key == 'view_table'):
        unique_context = getFormContext(request.values)
    # elif (key == 'view_graph'):
    #     unique_context = getFormContext(request.values)
    elif (key == 'view_all_results'):
        unique_context.update(viewAllResults_GetVars())


    ###########################################################
    ### Render
    return renderTemplateWithContext(key, unique_context)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
    )
