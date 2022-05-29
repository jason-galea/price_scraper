#!/usr/bin/python3

### Imports
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    flash,
    redirect,
)


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
}
page_titles = {
    "index":"Welcome to Price Scraper (TM)!",
    "scrape":"Scrape Data",
    "view_table":"View data in table",
    "view_graph":"View data in graph",
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

# @app.route("/scrape", methods=('GET', 'POST'))
# def scrape():
#     return render_template(
#         "children/scrape.html",
#         # page_info=page_info,
#         nav_info=nav_info,
#         form_labels=form_labels,
#         title=page_titles["scrape"],
#     )

@app.route("/view_table", methods=('GET', 'POST'))
def view_table():
    if (request.method == "POST"):
        website = request.form["website"]
        category = request.form["category"]

    return render_template(
        "children/view_table.html",
        # page_info=page_info,
        nav_info=nav_info,
        form_labels=form_labels,
        title=page_titles["view_table"],
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




if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
    )
