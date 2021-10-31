#!/usr/bin/python3

### Imports
# from logging import error
import time
# from typing import Dict
# from selenium import webdriver
# from bs4 import BeautifulSoup as bs

# import mysql.connector
# from mysql.connector import errorcode


### File Imports
from scrape import Table


### Functions
class Extract:
    def pccg(soup, table_index):
        data = []
        data_type = Table.NAMES[table_index]

        for product in soup.find_all('div', class_="product-container"):
            
            ### Common attributes
            # Data extracted from DOM
            p_title = product.find_next("a", class_="product-title").string
            p_url = product.find_next("a", class_="product-title").attrs["href"]
            # p_incomplete_desc = product.find_next("p").string
            p_price_aud = int(product.find_next("div", class_="price").string.strip("$")) # "$123" --> 123

            # Data extrapolated from previous extraction
            p_title_array = p_title.split()
            # p_incomplete_desc_array = p_incomplete_desc.split()
            p_hdd_capacity = int(next(x for x in p_title_array if x.__contains__("TB")).strip("TB")) # "10TB" --> 10
            p_hdd_price_per_tb = round(p_price_aud/p_hdd_capacity, 2) # Round to two decimal places

            # Brand/Series/Model fuckery, extrapolated from Title
            if p_title_array[0] == "Western":
                p_brand = "Western Digital"
                p_series = p_title_array[3] # "Blue"
                if p_series == "Red": # Logic to handle multi-word series names
                    p_series += " " + p_title_array[4] # "Red Plus"
                    p_model_number = p_title_array[6] # "WD8001FZBX"
                else:
                    # p_series is already correct
                    p_model_number = p_title_array[5]
            
            elif p_title_array[0] == "Seagate":
                p_brand = "Seagate"
                p_series = p_title_array[1] # "Ironwolf"
                p_model_number = p_title_array[3] # "ST8000VN004"
            
            # TODO: Separate common & unique attribute extraction logic.
            # Eg Title/price/URL are common attributes
            # HDD Capacity is unique

            # match data_type:
            #     case "HDD":
            #         p_hdd_capacity = int(next(x for x in p_title_array if x.__contains__("TB")).strip("TB")) # "10TB" --> 10
            #         p_hdd_price_per_tb = round(p_price_aud/p_hdd_capacity, 2)
            #     case _: # Default case
            #         pass

            data.append({
                "Time": time.strftime("%Y-%m-%d %H:%M:%S")
                , "Retailer": "PCCG"
                , "Title": p_title
                , "URL": p_url
                # , "IncompleteDescription": p_incomplete_desc
                , "PriceAUD": p_price_aud
                , "Brand": p_brand
                , "Series": p_series
                , "ModelNumber": p_model_number
                , "HDDCapacity": p_hdd_capacity
                , "HDDPricePerTB": p_hdd_price_per_tb
            })

        # Just sign-posting a lil' bit
        print("Success: Extracted data from PCCG {} webpage".format(data_type))
        # print()
        # print(data)
        # print()

        return data
