#!/usr/bin/python3

### Imports
import subprocess
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
# page_info = {
#     "index":{
#         "name":"Home",
#         "title":"Welcome to Price Scraper (TM)!",
#         # "title":"POTATO",
#         "path":"/",
#     },
#     "scrape":{
#         "name":"Scrape Data",
#         "title":"Scrape Data",
#         "path":"/scrape",
#     },
#     "view_table":{
#         "name":"View Table",
#         "title":"View data in table",
#         "path":"/view_table",
#     },
#     "view_graph":{
#         "name":"View Graph",
#         "title":"View data in graph",
#         "path":"/view_graph",
#     },
#     # "":{
#     #     "name":"",
#     #     "title":"",
#     #     "path":"",
#     # },
# }

nav_info = {
    "Home":"/",
    "Scrape Data":"/scrape",
    "View Table":"/view_table",
    "View Graph":"/view_graph",
    "View All Results":"/view_all_results",
}
page_titles = {
    "index":"Welcome to Price Scraper (TM)!",
    "scrape":"Scrape Data",
    "view_table":"View data in table",
    "view_graph":"View data in graph",
    "view_all_results":"View all existing result files",
}
form_labels = {
    "website":{
        "pccg":"PC Case Gear",
        "scorptec":"Scorptec",
        "centrecom":"Centre Com",
    },
    "category":{
        "hdd":"3.5\" Hard Drive",
        "ssd":"SSD",
        "cpu":"CPU",
        "gpu":"GPU",
    },
}



###########################################################
### Flask routes
### TODO: Explode this function into separate pages (and combine after logic complete?)
# @app.route("/", methods=('GET', 'POST'))
# @app.route("/<path:path>", methods=('GET', 'POST'))
# def routes(path="index"):
#     return render_template(
#         f"children/{path}.html",
#         page_info=page_info,
#         form_labels=form_labels,
#         title=page_info[path]['title'],
#     )

@app.route("/")
def index():
    return render_template(
        "children/index.html",
        # page_info=page_info,
        nav_info=nav_info,
        # form_labels=form_labels,
        title=page_titles["index"],
    )

@app.route("/scrape", methods=('GET', 'POST'))
def scrape():

    print(
        # request.values['website'] = {request.values['website']}
        # request.values['category'] = {request.values['category']}
        f"""
        request.values.__dict__ = {request.values.__dict__}
        len(request.values) = {len(request.values)}
        request.values.get('website') = {request.values.get('website')}
        request.values.get('category') = {request.values.get('category')}

        """
    )

    context = {
        "nav_info":nav_info,
        "form_labels":form_labels,
        "title":page_titles["scrape"],
    }

    # if (len(request.values) != 0):
    if (
        (request.values.get('website') != None)
        and (request.values.get('website') != None)
    ):
        context.update({
            "website": request.values.get('website'),
            "category": request.values.get('category'),
        })

        ### Start subprocess (async)
        print("\nStarting subprocess")
        # p = subprocess.Popen(['ls', '-lh'])
        # p = subprocess.Popen(['sleep', '3'])
        p = subprocess.Popen(['./script/scrape.py', 'pccg', 'hdd'])
        print("Waiting for subprocess to complete...")

        ### Wait for output
        # p.communicate() #now wait plus that you can send commands to process
        

    return render_template(
        template_name_or_list="children/scrape.html",
        **context,
    )

@app.route("/view_table", methods=('GET', 'POST'))
def view_table():

    # print(
    #     f"""
    #     request.values.__dict__ = {request.values.__dict__}
    #     len(request.values) = {len(request.values)}
    #     request.values.get('website') = {request.values.get('website')}
    #     request.values.get('category') = {request.values.get('category')}

    #     """
    # )

    context = {
        "nav_info":nav_info,
        "form_labels":form_labels,
        "title":page_titles["view_table"],
    }

    if (len(request.values) != 0):
        context.update({
            "website": request.values.get('website'),
            "category": request.values.get('category'),
        })

    return render_template(
        template_name_or_list="children/view_table.html",
        **context,
    )

# @app.route("/view_graph", methods=('GET', 'POST'))
# def view_graph():
#     return render_template(
#         "children/view_graph.html",
#         # page_info=page_info,
#         nav_info=nav_info,
#         form_labels=form_labels,
#         title=page_titles["view_graph"],
#     )

@app.route("/view_all_results")
def view_all_results():

    # result = subprocess.run(
    #     ['ls', '-lh'],
    #     stdout=subprocess.PIPE,
    #     encoding='text')
    result = subprocess.check_output(
        ['ls', '-lh', './out/'],
        encoding='utf-8').split('\n')
    # print(
    #     f"""
    #     result = {result}
    #     result.stdout = {result.stdout}
    #     result.stderr = {result.stderr}
    #     """
    # )
    context = {
        "nav_info": nav_info,
        "form_labels": form_labels,
        "title": page_titles["view_all_results"],
        # "ls_stdout": result.stdout,
        "ls_stdout": result,
    }

    return render_template(
        template_name_or_list="children/view_all_results.html",
        **context,
    )



if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
    )
