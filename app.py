#!/usr/bin/env python3

import os
import json
import datetime
import html
import threading
import pandas as pd
# import psycopg2
# import sqlalchemy

from flask import Flask, render_template, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy

# from glob import glob
# from selenium.common.exceptions import WebDriverException

# import lib.Extract as Extract
from lib.PCCG import PCCG
from lib.Scorptec import Scorptec
from lib.CentreCom import CentreCom


###########################################################
### GLOBAL VARS
app = Flask(__name__)

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

app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS "] = False
db = SQLAlchemy(app)


###########################################################
### Generic functions
# def get_json_filenames() -> list:
#     return glob(f"{JSON_OUTPUT_DIR}/*.json")

def listContainsAllValues(haystack, needles) -> bool:
    return all((n in haystack) for n in needles)


###########################################################
### Route-specific functions
def scrape_start_extract_thread(website, category) -> None:

    ### TODO: Check if another thread is already running
    # if (???):
    #     print(f"\n==> ERROR: Another thread is already running, please wait a moment for it to finish")
    #     return

    NOW = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    # JSON_OUTPUT_FILE = f"{JSON_OUTPUT_DIR}/{NOW}_{website}_{category}.json"

    match website:
        case "pccg": website_class = PCCG
        case "scorptec": website_class = Scorptec
        case "centrecom": website_class = CentreCom

    # print(f"\n==> INFO: Scraping with website '{website}' and category '{category}'")
    scrape_thread = threading.Thread(
        target=website_class,
        # args=(category, JSON_OUTPUT_DIR, JSON_OUTPUT_FILE),
        args=(category),
    )

    print(f"==> INFO: Launching thread to scrape '{category}' data from '{website}'")
    scrape_thread.start()
    # while True:
    #     try:
    #         scrape_thread.start()
    #         break
    #     except WebDriverException as e:
    #         print(f"\n==> WARN: WebDriverException exception raised: '{e}'")
    #         print(f"\n==> WARN: This was most likely caused by conflicting threads")
    #         print(f"\n==> WARN: Restarting thread")
    #         continue


def table_get_template_vars(website, category) -> dict:

    # ### Filter to files containing the chosen website & category
    # filtered_files = [ item
    #     for item in get_json_filenames()
    #     if (listContainsAllValues(item.split('.')[0].split("_"), [website, category]))
    # ]
    # # print(f"filtered_files = {filtered_files}")
    # latest_file = max(filtered_files, key=os.path.getctime)
    # latest_file_basename = os.path.basename(latest_file)

    ### DEBUG
    # print(f"latest_file = {latest_file}")
    # print(f"latest_file_basename = {latest_file_basename}")

    # ### Read JSON --> DataFrame
    # df: pd.DataFrame = pd.read_json(latest_file)


    ### TODO: Query DB for latest entry for website & category
    utctime_for_latest_matching_data = "asd"
    
    ### TODO: Query DB for data matching above UTCtime
    df = pd.read_sql_query()


    df['Title'] = df.apply(table_fix_title_col, axis=1)
    df['TitleLink'] = df.apply(
        lambda row: f"<a href={row['URL']}>{row['Title']}</a>",
        axis=1,
    )

    ### Restrict & sort cols
    df = df[TABLE_COLS[category]['display_cols']]
    df = df.sort_values(TABLE_COLS[category]['sort_col'], ignore_index=True)

    ### Escape all cols except "TitleLink"
    df[[
        c
        for c in list(df.columns)
        if (c != 'TitleLink')
    ]].apply( html.escape, axis=1 )

    return {
        # 'latest_file': latest_file,
        # 'latest_file_basename': latest_file_basename, ### Signposting
        'table_html': df.to_html(escape=False)
    }


def table_fix_title_col(row) -> str:
    match_replace_dict = {
        'Hard Drive': 'HDD',
        '3.5in ': '',
        'WD ': '',
    }
    result = str(row["Title"])
    
    for match, replace in match_replace_dict.items():
        result = result.replace(match, replace)

    return result

def test_db():

    ### hehehe
    # postgress_engine = sqlalchemy.create_engine(POSTGRES_DB_URI)

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
                scrape_start_extract_thread(website, category)

        case "table":
            if FORM_IS_VALID:
                page_vars.update( table_get_template_vars(website, category) )

        case "graph":
            pass
            test_db() ### DEBUGGING

        case "results":

            # results = [os.path.basename(s) for s in get_json_filenames()]
            # results.sort(reverse=True) ### Sort by reverse date, newest items on top
            results = ["no_json_files_anymore_teehee!!"]

            page_vars.update({ 'results': results })



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


# if __name__ == '__main__':
#     app.run(
#         # debug=True,
#         host='0.0.0.0',
#     )
