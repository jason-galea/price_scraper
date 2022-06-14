#!/usr/bin/python3

### Imports
from multiprocessing import context
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
    "form_test":"A TEST PAGE, FOR TESTING FORMS. TEST",
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


### Routes
@app.route("/", methods=('GET', 'POST'))
def index():

    context = {
        "nav_info":nav_info,
        "form_labels":form_labels,
        # "title":page_titles["form_test"],
        "title":page_titles["index"],
    }

    if (request.method == "POST"):
        context.update({
            "website": request.form["website"],
            "category": request.form["category"],
        })

    return render_template(
        template_name_or_list="children/form_test.html",
        **context,
    )



### Main
if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
    )
