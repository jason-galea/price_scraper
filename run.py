#!/usr/bin/python3

### Imports
from cProfile import label
from unittest import result
from flask import Flask, render_template


### Vars
app = Flask(__name__)
page_info = {
    "index":{
        "name":"Home",
        "title":"Welcome to Price Scraper (TM)!",
        "path":"/",
    },
    "scrape":{
        "name":"Scrape Data",
        "title":"Scrape Data",
        "path":"/scrape",
    },
    "view_table":{
        "name":"View Table",
        "title":"View data in table",
        "path":"/view_table",
    },
    "view_graph":{
        "name":"View Graph",
        "title":"View data in graph",
        "path":"/view_graph",
    },
    # "":{
    #     "name":"",
    #     "title":"",
    #     "path":"",
    # },
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
### TODO: Explode this function back into separate pages, combine after logic is final
@app.route("/")
@app.route("/<path:path>")
def routes(path="index"):
    return render_template(
        f"children/{path}.html",
        page_info=page_info,
        form_labels=form_labels,
        title=page_info[path]['title'],
    )

# @app.route("/")
# def index():
#     return render_template(
#         "children/index.html",
#         page_info=page_info,
#         form_labels=form_labels,
#         title=page_info["index"]['title'],
#     )

# @app.route("/scrape")
# def scrape():
#     return render_template(
#         "children/scrape.html",
#         page_info=page_info,
#         form_labels=form_labels,
#         title=page_info["scrape"]['title'],
#     )

# @app.route("/view_table")
# def view_table():
#     return render_template(
#         "children/view_table.html",
#         page_info=page_info,
#         form_labels=form_labels,
#         title=page_info["view_table"]['title'],
#     )

# @app.route("/view_graph")
# def view_graph():
#     return render_template(
#         "children/view_graph.html",
#         page_info=page_info,
#         form_labels=form_labels,
#         title=page_info["view_graph"]['title'],
#     )




if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
    )
