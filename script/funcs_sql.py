#!/usr/bin/python3

### Imports
from logging import error
# import time
# from typing import Dict
# from selenium import webdriver
# from bs4 import BeautifulSoup as bs

import mysql.connector
from mysql.connector import errorcode


### File Imports
import scrape


### Functions
def sql_create_database(cursor):
    try:
        # No need for "IF NOT EXISTS", because this function is only called to OVERWRITE a corrupt DB? I think?
        # cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(SQL_DB))
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(scrape.SQL_DB))
        print("Success: Created database {}".format(scrape.SQL_DB))
    except mysql.connector.Error as err:
        print("Failure: Could not create database: \n{}".format(err.msg))
        exit(1)

def sql_drop_tables(cursor):
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        for name in scrape.SQL_TABLE_NAMES:
            cursor.execute("DROP TABLE IF EXISTS {}".format(name))
            print("Success: Dropped table {}".format(name)) # Will "succeed" even if table was already dropped.

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    except mysql.connector.Error as err:
        print("Failure: Could not drop tables: \n{}".format(err.msg))
        exit(1)

def sql_create_tables(cursor):
    for name in scrape.SQL_TABLE_NAMES:
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(name, scrape.SQL_TABLE_SCHEMAS[name]))
            print("Success: Created table {}".format(name))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Warning: Table {} already exists".format(name))
            else:
                print("Failure: Could not create table {}: \n{}".format(name, err.msg))
                # exit(1)

def sql_insert_into_hdd(cursor, data):
    # Accepts an array of dicts
    # Each dict is one row
    data_type = "HDD" # AKA. table name

    try:
        for x in data:
            # I know this is redundant, but it greatly simplifies troubleshooting
            insert_string = "INSERT INTO {} VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                data_type 
                , x["Time"]
                , x["Retailer"]
                , x["Title"]
                , x["URL"]
                , x["PriceAUD"]
                , x["Brand"]
                , x["Series"]
                , x["ModelNumber"]
                , x["HDDCapacity"]
                , x["HDDPricePerTB"]
            )
            print("\nINSERT STRING:\n{}\n".format(insert_string))

            cursor.execute(insert_string)
            print("Success: Inserted data into table {}".format(data_type))

    except mysql.connector.Error as err:
        print("Failure: Could not insert data into table {}: \n{}".format(data_type, err.msg))
        exit(1)

def sql_select_all_from_table(table_index):
    name = scrape.SQL_TABLE_NAMES[table_index]
    pass