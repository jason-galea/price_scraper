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

### NOTE: Would this be better as a pd.DataFrame?
### NOTE: Jinja can work with dataframes without imports... hmmm
PAGE_INFO = {
    'index':{
        'route':'/',
        'template':'children/index.html',
        'title':'Home',
        # 'desc':'Welcome to Price Scraper (TM)!',
        'desc':[
            'Welcome to Price Scraper (TM)!',
            'This website will scrape & display the latest price/specs/etc. of computer hardware.',
            'It\'s designed to work with specific Australian computer parts retailers.',
        ],
    },
    'scrape':{
        'route':'/scrape',
        'template':'children/scrape.html',
        # 'title':'Scrape Data',
        'title':'Scrape',
        # 'desc':'Collect new product data from a chosen website',
        'desc':[
            'This page lets you scrape the latest data from your chosen website & category.',
            'Make a selection and press "Submit" to continue.',
            'This will launch a subprocess, which will run in the background.',
            'To verify that the job was successful, head to the "Results" page.',
        ],
    },
    'view_table':{
        'route':'/view_table',
        'template':'children/view_table.html',
        # 'title':'View Table',
        'title':'Table',
        # 'desc':'View collected data in table',
        'desc':[
            'This page allows you to view the most recent result for a given website & category.',
            'The data will be displayed in a table.',
            'Make a selection and press "Submit" to continue.',
        ],
    },
    'view_graph':{
        'route':'/view_graph',
        'template':'children/view_graph.html',
        # 'title':'View Graph',
        'title':'Graph',
        # 'desc':'View collected data in graph',
        'desc':[
            'This page allows you to view the most recent result for a given website & category.',
            'The data will be displayed in a graph.',
            'Make a selection and press "Submit" to continue.',
        ],
    },
    'view_all_results':{
        'route':'/view_all_results',
        'template':'children/view_all_results.html',
        # 'title':'View All Results',
        'title':'Results',
        # 'desc':'View all existing result files',
        'desc':[
            'This page shows every result currently saved on the webserver.',
            '''If no results are found, or if the "ls -lh ./out/" subprocess fails, try
            scraping some more data on the "Scrape" page.''', ### Strings. Gross :(((
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
### Functions
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


###########################################################
### Flask routes
### TODO: Explode this function into separate pages (and combine after logic complete?)
# @app.route('/', methods=['GET', 'POST'])
# @app.route('/<path:path>', methods=['GET', 'POST'])
# # def routes(path='index'):
# def routes(key='index'):
#     # return render_template(
#     #     f"children/{path}.html",
#     #     page_info=page_info,
#     #     form_labels=form_labels,
#     #     title=page_info[path]['title'],
#     # )

#     if (key in ['', '', '', ''])
#         ### Get form vars
#         unique_context = getFormContext(request.values)

#     ### Render
#     return renderTemplateWithContext(key, unique_context)

@app.route('/')
def index():
    return renderTemplateWithContext('index')

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():

    key = 'scrape'

    ### Get form vars
    unique_context = getFormContext(request.values)

    ### Start subprocess, if args are defined
    if all ((k in unique_context) for k in ['website', 'category']):
        cmd = './script/scrape.py pccg hdd' ### Much cleaner

        ### Run & block
        # p = sp.run(scrape_command.split())

        ### Run & wait
        p = sp.Popen(cmd.split())
        # p.communicate() ### Print STDOUT to console

    return renderTemplateWithContext(key, unique_context)


@app.route("/view_table", methods=['GET', 'POST'])
def view_table():

    key = 'view_table'

    ### Get form vars
    unique_context = getFormContext(request.values)

    ### Render
    return renderTemplateWithContext(key, unique_context)


@app.route("/view_graph", methods=['GET', 'POST'])
def view_graph():

    key = 'view_graph'

    ### Get form vars
    unique_context = getFormContext(request.values)

    ### Render
    return renderTemplateWithContext(key, unique_context)


@app.route("/view_all_results")
def view_all_results():

    key = 'view_all_results'

    ### Get form vars
    unique_context = getFormContext(request.values)


    ### Get unique vars
    try:
        cmd = 'ls -lh ./out/'
        result = sp.check_output( cmd.split(), encoding='utf-8' ).split('\n')
        sp_success = True
    except sp.CalledProcessError as e:
        result = [e] ### The template expects a list
        sp_success = False

    unique_context.update({
        'ls_stdout':result,
        'sp_success':sp_success
    })

    ### Render
    return renderTemplateWithContext(key, unique_context)


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
    )
