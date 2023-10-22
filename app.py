#!/usr/bin/env python3

import os
import json
import html
import pandas as pd

from flask import Flask, render_template, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.generic_funcs import *
from src.Pages.Scrape import Scrape
from src.Pages.Table import Table


###########################################################
### Create Flask app & db
class Base(DeclarativeBase):
    pass

app = Flask(__name__)
db = SQLAlchemy(model_class=Base)


###########################################################
### GLOBAL VARS
ROOT = app.root_path

with open(f"{ROOT}/conf/page_info.json", "r") as f: PAGE_INFO = json.load(f)
with open(f"{ROOT}/conf/form_labels.json", "r") as f: FORM_LABELS = json.load(f)
with open(f"{ROOT}/conf/table_cols.json", "r") as f: TABLE_COLS = json.load(f)

FORM_COLS = ['website', 'category']

POSTGRES_HOST        = os.environ['POSTGRES_HOST']
POSTGRES_PORT        = os.environ['POSTGRES_PORT']
POSTGRES_USER        = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD    = os.environ['POSTGRES_PASSWORD']
POSTGRES_DB          = os.environ['POSTGRES_DB']

# POSTGRES_DB_URI = "db+psycopg2://root:postgress@db:5432/bookstore"
POSTGRES_DB_URI = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'


###########################################################
### Configure Flask app & initialise db
app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS "] = False

db.init_app(app)

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String)

with app.app_context():
    db.create_all()



###########################################################
### Flask routes
@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def routes(path='index'):

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

    FORM_IS_VALID = listContainsAllValues(page_vars.keys(), FORM_COLS)
    if FORM_IS_VALID:
        website = page_vars['website']
        category = page_vars['category']

    match path:
        case "index":
            pass

        case "scrape":
            if FORM_IS_VALID:
                # scrape_start_extract_thread(website, category)
                Scrape.start_extract_thread(website, category)

        case "table":
            if FORM_IS_VALID:
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

            print(f"==> DEBUG: POSTGRES_DB_URI = {POSTGRES_DB_URI}")

            # def connect():
            #     return psycopg2.connect(
            #         host=host,
            #         port=port,
            #         user=user,
            #         password=password,
            #         dbname=db,
            #         # sslmode='require',
            #     )

            # # engine = sqlalchemy.create_engine('redshift+psycopg2://', creator=connect)
            # engine = sqlalchemy.create_engine('postgresql://', creator=connect)
            # conn = engine.connect()
            
            # statement = sqlalchemy.select([sqlalchemy.literal(1234)])
            # print(conn.execute(statement).fetchall())
            
            # global POSTGRESS_CONN
            # POSTGRESS_CONN = postgress_engine.connect()

            # res = POSTGRESS_CONN.execute("SELECT * FROM pg_catalog.pg_tables;")
            # print(res)



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
        path='favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )
