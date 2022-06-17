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

# nav_info = {
#     "Home":"/",
#     "Scrape Data":"/scrape",
#     "View Table":"/view_table",
#     "View Graph":"/view_graph",
#     "View All Results":"/view_all_results",
# }
# page_titles = {
#     "index":"Welcome to Price Scraper (TM)!",
#     "scrape":"Scrape Data",
#     "view_table":"View data in table",
#     "view_graph":"View data in graph",
#     "view_all_results":"View all existing result files",
# }

### NOTE: Would this be better as a pd.DataFrame?
### NOTE: Jinja can work with dataframes without imports... hmmm
PAGE_INFO = {
    'index':{
        'route':'/',
        'template':'children/index.html',
        'title':'Home',
        'desc':'Welcome to Price Scraper (TM)!',
    },
    'scrape':{
        'route':'/scrape',
        'template':'children/scrape.html',
        'title':'Scrape Data',
        'desc':'Collect new product data from a chosen website',
    },
    'view_table':{
        'route':'/view_table',
        'template':'children/view_table.html',
        'title':'View Table',
        'desc':'View collected data in table',
    },
    'view_graph':{
        'route':'/view_graph',
        'template':'children/view_graph.html',
        'title':'View Graph',
        'desc':'View collected data in graph',
    },
    'view_all_results':{
        'route':'/view_all_results',
        'template':'children/view_all_results.html',
        'title':'View All Results',
        'desc':'View all existing result files',
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

# COMMON_CONTEXT = {
#     'nav_info':nav_info,
#     'form_labels':form_labels,
#     'title':page_titles['scrape'],
# }




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
        'PAGE_INFO':PAGE_INFO
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
# def routes(path='index'):
#     return render_template(
#         f"children/{path}.html",
#         page_info=page_info,
#         form_labels=form_labels,
#         title=page_info[path]['title'],
#     )


@app.route('/')
def index():
    return renderTemplateWithContext('index')

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():

    ### Get form vars
    unique_context = getFormContext(request.values)

    ### Start subprocess, if args are defined
    if all ((key in unique_context) for key in ['website', 'category']):
        cmd = './script/scrape.py pccg hdd' ### Much cleaner

        ### Run & block
        # p = sp.run(scrape_command.split())

        ### Run and wait
        p = sp.Popen(cmd.split())
        # p.communicate() ### Print STDOUT to console 

    return renderTemplateWithContext('scrape', unique_context)


@app.route("/view_table", methods=['GET', 'POST'])
def view_table():

    ### Get form vars
    unique_context = getFormContext(request.values)

    ### Render
    return renderTemplateWithContext('view_table', unique_context)


@app.route("/view_graph", methods=['GET', 'POST'])
def view_graph():

    ### Get form vars
    unique_context = getFormContext(request.values)

    ### Render
    return renderTemplateWithContext('view_graph', unique_context)


@app.route("/view_all_results")
def view_all_results():

    ### Get form vars
    unique_context = getFormContext(request.values)

    ### Get unique vars
    try:
        cmd = 'ls -lh ./out/'
        result = sp.check_output( cmd.split(), encoding='utf-8' ).split('\n')
    except sp.CalledProcessError as e:
        result = ['Exception raised from subprocess:', e] ### The template expects a list

    unique_context.update({ 'ls_stdout':result })

    ### Render
    return renderTemplateWithContext('view_all_results', unique_context)


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
    )
