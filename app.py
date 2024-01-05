#!/usr/bin/env python3

"""
A Flask-based webserver which extracts PC component data from Australian retailers.
"""

import os
import json

from flask import Flask, render_template, request, send_from_directory
from flask_migrate import Migrate

from src.config import PAGE_INFO, FORM_LABELS
# from src.generic_funcs import list_contains_all_values
from src.Pages.Scrape import Scrape
from src.Pages.Table import Table
from src.Database import db

### DB Models/Tables to create
from src.Database import SSD, HDD, DDR4, DDR5


###########################################################
### GLOBALS
HOST        = os.environ['POSTGRES_HOST']
PORT        = os.environ['POSTGRES_PORT']
USER        = os.environ['POSTGRES_USER']
PASSWORD    = os.environ['POSTGRES_PASSWORD']
DB_NAME     = os.environ['POSTGRES_DB']

POSTGRES_DB_URI = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

app: Flask = Flask(__name__)


def run_app():
    """Configure & run Flask app, initialise DB."""

    app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_DB_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS "] = False ### Silence warning

    db.init_app(app)
    _migrate = Migrate(app, db)

    ### Create models & tables
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0")


@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def routes(path='index'):
    """
    Function to serve all routes (except /favicon.ico).\n
    Accepts the path of whatever page was requested.\n
    Handles form inputs, gathers vars required to template HTML.\n
    Returns templated HTML.
    """

    # key = path ### Deal with it
    common_vars = {
        'PAGE_INFO': PAGE_INFO,
        'key': path,
        'template_name_or_list': PAGE_INFO[path]['template'],
        'desc': PAGE_INFO[path]['desc'],
    }
    page_vars = {
        "FORM_LABELS": FORM_LABELS,
        **request.form,
    }

    # form_is_valid = list_contains_all_values(page_vars, ['website', 'category'])
    form_is_valid = ("website" in page_vars) and ("category" in page_vars)
    if form_is_valid:
        website = page_vars['website']
        category = page_vars['category']

        # print(f"==> DEBUG: website = {website}")
        # print(f"==> DEBUG: category = {category}")

    match path:
        case "index":
            pass

        case "scrape":
            if form_is_valid:
                Scrape.start_extract_thread(app, website, category)

        case "table":
            if form_is_valid:
                page_vars.update( Table.get_template_vars(website, category) )

        case "graph":
            pass

        # ### TODO: Delete this page?
        # case "results":

        #     # results = [os.path.basename(s) for s in get_json_filenames()]
        #     # results.sort(reverse=True) ### Sort by reverse date, newest items on top
        #     results = ["no_json_files_anymore_teehee!!"]

        #     page_vars.update({ 'results': results })

        case "test":

            # products: list = SSD.get_most_recent(SSD, "pccg")
            products: list = SSD.get_most_recent("pccg")
            # print(f"==> DEBUG: {most_recent_products=}")
            # for ssd in most_recent_products:
            #     print(f"==> DEBUG: {ssd["Title"]=}")
            #     # print(f"==> DEBUG: {ssd.utctime=}")
            print(f"==> DEBUG: products[0] = {json.dumps(products[0], indent=4)}")

    ### DEBUG
    # print(f"\npage_vars: \n{json.dumps(page_vars, indent=2)}\n")


    ###########################################################
    ### Render
    return render_template(
        **common_vars,
        **page_vars,
    )


@app.route('/favicon.ico')
def favicon():
    """Favicon route"""
    return send_from_directory(
        directory=os.path.join(app.root_path, 'static'),
        path='favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )


if __name__ == "__main__":
    run_app()
