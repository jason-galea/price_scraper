#!/usr/bin/python3

### Imports
import sys
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
    "FORM TEST POST":"/",
    "Scrape Data":"/scrape",
    "View Table":"/view_table",
    "View Graph":"/view_graph",
}
page_titles = {
    "index":"Welcome to Price Scraper (TM)!",
    "scrape":"Scrape Data",
    "view_table":"View data in table",
    "view_graph":"View data in graph",
    "form_test":"FORM TEST POST",
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

    print(
        # request.form.__dict__ = {request.form.__dict__}
        # request.args.__dict__ = {request.args.__dict__}
        # request.form.get.__dict__ = {request.args.__dict__}
        f"""
        request.values.__dict__ = {request.values.__dict__}
        request.values.__len__ = {request.values.__len__}
        len(request.values) = {len(request.values)}
        request.values.get('website') = {request.values.get('website')}
        request.values.get('category') = {request.values.get('category')}
        

        """
    )

    context = {
        "nav_info":nav_info,
        "form_labels":form_labels,
        "title":page_titles["form_test"],
    }

    if (len(request.values) != 0):
        context.update({
            "website": request.values.get('website'),
            "category": request.values.get('category'),
        })

    return render_template(
        template_name_or_list="children/form_test_POST.html",
        **context,
    )



### Main
if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
    )

    # try:
    #     app.run(
    #         debug=True,
    #         host='0.0.0.0',
    #     )
    # except SystemExit:
    #     print("Encountered SystemExit")
