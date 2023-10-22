#!/usr/bin/env python3

### https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/

import os

from flask import Flask, render_template, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.config import PAGE_INFO, FORM_LABELS
from src.generic_funcs import list_contains_all_values
from src.Pages.Scrape import Scrape
from src.Pages.Table import Table


# ### DEBUG
# import debugpy
# debugpy.listen(('0.0.0.0', 5678))
# debugpy.wait_for_client()
# debugpy.breakpoint()


###########################################################
### GLOBALS
host        = os.environ['POSTGRES_HOST']
port        = os.environ['POSTGRES_PORT']
user        = os.environ['POSTGRES_USER']
password    = os.environ['POSTGRES_PASSWORD']
db_name     = os.environ['POSTGRES_DB']

POSTGRES_DB_URI = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"


###########################################################
### Init db
class Base(DeclarativeBase):
    pass

db: SQLAlchemy = SQLAlchemy(model_class=Base)


###########################################################
### Init Flask
app: Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_DB_URI
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS "] = False

db.init_app(app)


###########################################################
### Define models
class Product(db.Model):
    """
    SQLAlchemy model, specifying the schema for table "products"
    """
    __tablename__ = "products"

    id: Mapped[int]             = mapped_column(Integer, primary_key=True, unique=True)
    utctime: Mapped[DateTime]   = mapped_column(DateTime, nullable=False)
    retailer: Mapped[String]    = mapped_column(String, nullable=False)



###########################################################
### Create tables
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
            pass

            # print(f"==> DEBUG: POSTGRES_DB_URI = {POSTGRES_DB_URI}")

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
        # directory=f"{CWD}/static/",
        path='favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )
