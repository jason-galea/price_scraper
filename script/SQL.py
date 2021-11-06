#!/usr/bin/python3

### Imports
from logging import error
import mysql.connector
from mysql.connector import errorcode

# File Imports
from Table import Table


class SQL:
    ### Static variables
    # TODO: Move these details to a .txt file in ~/
    # HOST = "localhost"
    HOST = "127.0.0.1"
    # HOST = "10.1.1.160"
    USER = "scraper"
    PASS = "Password##123" # Oh no!!!
    DB = "PriceScraper"

    ### Init
    def __init__(self) -> None:
        self.cnx = mysql.connector.connect(
            host=self.HOST
            , user=self.USER
            , password=self.PASS
            , database=self.DB
        )
        self.cursor = self.cnx.cursor()
        print("Success: Connected to MySQL on {}".format(self.HOST))

    ### Functions
    def use_database(self):
        try:
            self.cursor.execute("USE {}".format(SQL.DB))
            # self.cnx.database = SQL.DB
        except mysql.connector.Error as err:
            print("Failure: Database {} does not exist".format(SQL.DB))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                SQL.create_database()
                print("Success: Database {} created".format(SQL.DB))
                self.cursor.execute("USE {}".format(SQL.DB))
                # self.cnx.database = SQL.DB
            else:
                print(err.msg) # This error would be non-specific, so I can't describe it beforehand
                exit(1)
        print("Success: Now using database {}".format(SQL.DB))
        # return cnx

    def create_database(self):
        try:
            # No need for "IF NOT EXISTS", because this function is only called to OVERWRITE a corrupt DB? I think?
            # cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(DB))
            self.cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(SQL.DB))
            print("Success: Created database {}".format(SQL.DB))
        except mysql.connector.Error as err:
            print("Failure: Could not create database: \n{}".format(err.msg))
            exit(1)

    # def drop_tables(self):
    #     try:
    #         self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

    #         for name in Table.NAMES:
    #             self.cursor.execute("DROP TABLE IF EXISTS {}".format(name))
    #             print("Success: Dropped table {}".format(name)) # Will "succeed" even if table was already dropped.

    #         self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    #     except mysql.connector.Error as err:
    #         print("Failure: Could not drop tables: \n{}".format(err.msg))
    #         exit(1)

    def create_tables(self):
        for name in Table.NAMES:
            try:
                self.cursor.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(name, Table.SCHEMAS[name]))
                print("Success: Created table {}".format(name))
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("Warning: Table {} already exists".format(name))
                else:
                    print("Failure: Could not create table {}: \n{}".format(name, err.msg))
                    # exit(1)

    def select_all_from_table(self, name):
        pass

    def close(self):
        self.cnx.close()

    
    ### Child class
    class Insert:
        @staticmethod
        def hdd(data, cnx):
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
                    # print("\nINSERT STRING:\n{}\n".format(insert_string))

                    cnx.cursor().execute(insert_string)
                    cnx.commit()
                    print("Success: Inserted data into table {}".format(data_type))

            except mysql.connector.Error as err:
                print("Failure: Could not insert data into table {}: \n{}".format(data_type, err.msg))
                exit(1)


