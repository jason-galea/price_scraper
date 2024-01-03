#!/usr/bin/env python3

"""
A Flask-based webserver which extracts PC component data from Australian retailers.
"""

### https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/

import os

from flask import Flask, render_template, request, send_from_directory
# from flask_sqlalchemy import SQLAlchemy
# from flask_sqlalchemy.query import Query
# from sqlalchemy import Integer, String, DateTime
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_migrate import Migrate

from src.config import PAGE_INFO, FORM_LABELS
from src.generic_funcs import list_contains_all_values
from src.Pages.Scrape import Scrape
from src.Pages.Table import Table
from src.Database import db, SSD
# from src.Database.Product import Product


# ### DEBUG
# import debugpy
# debugpy.listen(('0.0.0.0', 5678))
# debugpy.wait_for_client()
# debugpy.breakpoint()


###########################################################
### GLOBALS
# app: Flask = Flask(__name__) ### Avoid "from app import app"

host        = os.environ['POSTGRES_HOST']
port        = os.environ['POSTGRES_PORT']
user        = os.environ['POSTGRES_USER']
password    = os.environ['POSTGRES_PASSWORD']
db_name     = os.environ['POSTGRES_DB']

POSTGRES_DB_URI = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"


###########################################################
### Init Flask
### TODO: Move this to a function
app: Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_DB_URI
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS "] = False

db.init_app(app)
# from src.Database.Product import Product
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()


# def run_app():
#     """
#     App entrypoint, used to configure DB and launch flask
#     """

#     app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_DB_URI

#     ### DB stuff
#     db.init_app(app)
#     # from src.Database.Product import Product
#     _migrate = Migrate(app, db)

#     with app.app_context():
#         db.create_all()

#     # return app
#     # app.run(debug=True, host="0.0.0.0", port=5000)
#     app.run(host="0.0.0.0")


@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def routes(path='index'):

    # key = path ### Deal with it
    common_vars = {
        'PAGE_INFO': PAGE_INFO,
        'key': path,
        'template_name_or_list': PAGE_INFO[path]['template'],
        # 'template_name_or_list': f"{CWD}/templates/{PAGE_INFO[path]['template']}",
        'desc': PAGE_INFO[path]['desc'],
    }
    page_vars = {
        "FORM_LABELS": FORM_LABELS,
        **request.form,
    }

    form_is_valid = list_contains_all_values(page_vars.keys(), ['website', 'category'])
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
                # scrape_start_extract_thread(website, category)
                Scrape.start_extract_thread(app, db, website, category)

        case "table":
            if form_is_valid:
                # page_vars.update( table_get_template_vars(website, category) )
                page_vars.update( Table.get_template_vars(website, category) )

        case "graph":
            pass

        ### TODO: Delete this page?
        case "results":

            # results = [os.path.basename(s) for s in get_json_filenames()]
            # results.sort(reverse=True) ### Sort by reverse date, newest items on top
            results = ["no_json_files_anymore_teehee!!"]

            page_vars.update({ 'results': results })

        case "test":

            most_recent_products: list = Product.get_most_recent("pccg", "ssd")
            print(f"==> DEBUG: {most_recent_products=}")
            for ssd in most_recent_products:
                print(f"==> DEBUG: {ssd.Title=}")
                # print(f"==> DEBUG: {ssd.utctime=}")

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
    return send_from_directory(
        directory=os.path.join(app.root_path, 'static'),
        # directory=f"{CWD}/static/",
        path='favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )
