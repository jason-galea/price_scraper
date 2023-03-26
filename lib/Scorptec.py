# import os
import datetime
# import enum
import json
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver import Firefox, DesiredCapabilities
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from lib.common import *


class Scorptec:
    CATEGORY_URLS = {
        "hdd": "https://www.scorptec.com.au/product/hard-drives-&-ssds/hdd-3.5-drives",
        "ssd": "https://www.scorptec.com.au/product/hard-drives-&-ssds/solid-state-drives-ssd",
        # "cpu": "",
        # "gpu": "",
    }

    def __init__(self, category, output_dir, output_file, debug=False) -> None:
        base_url = self.CATEGORY_URLS[category]
        driver = instantiate_ff_driver_and_download(base_url)
        
        bs4_html_parser_list = self._get_html_parser_list(driver, base_url)

        extracted_data = self._extract(category, bs4_html_parser_list)

        if (debug):
            print(json.dumps(extracted_data, indent=4))

        export_json(extracted_data, output_dir, output_file)

    def _get_html_parser_list(self, driver: Firefox, base_url: str) -> list:

        last_page = int(driver.find_element(By.ID, "total-page").text)
        result = []

        ### Fetch all page sources
        for current_page in range(1, last_page + 1):
            if (current_page != 1):
                driver.delete_all_cookies() ### Workaround for anti-bot nonsense
                driver.get(f"{base_url}?page={current_page}")

            ### Pagination fun!!!1!!!!
            ### TODO: Fix these lol, they simply do not work
            ### 90 items per page
            # select_dropdown = Select(driver.find_element(By.ID, "pagination-view-count"))
            # select_dropdown.select_by_visible_text("90")
            
            # ### Sort by price, low to high
            # sort_dropdown = Select(driver.find_element(By.ID, "widget-sort"))
            # sort_dropdown.select_by_visible_text("Price (low to high)")

            ### Find current page
            current_page_element = WebDriverWait(driver, 10).until(
                lambda x: x.find_element(By.ID, "current-page")
            )
            current_page = int(current_page_element.text)
            print(f"==> INFO: Opened page {current_page}/{last_page}")

            # ### Print product URLs
            # count = 0
            # for element in driver.find_elements(
            #     by=By.XPATH,
            #     value="//div[@class='detail-product-title']/a[contains(@href,'product') and @class='inherit-class']",
            # ):
            #     count += 1
            #     # product_elements.append(element)
            #     print(f"element.text = '{element.text}'")
            # print(f"==> INFO: Found {count} products on page {current_page}/{last_page}")

            ### Save HTML parser objects
            result.append(
                BeautifulSoup(
                    markup=driver.page_source,
                    features="html.parser"
                )
            )

        return result

    ### TODO: Move this into base class/common function
    def _extract(self, category: str, bs4_html_parser_list: list) -> list:
        match category:
            case "hdd":
                return self._extract_hdd_data(bs4_html_parser_list)
            case "ssd":
                return self._extract_ssd_data(bs4_html_parser_list)

    # @staticmethod
    def _extract_hdd_data(self, bs4_html_parser_list: list) -> list:
        results = []

        for bs4_html_parser in bs4_html_parser_list:
            for product in bs4_html_parser.find_all():
                # temp_result = self._get_common_data(product)
                temp_result = {}
                
                # print(f"==> Extracting data from '{???}'")

                # ### Print product URLs
                # count = 0
                # for element in driver.find_elements(
                #     by=By.XPATH,
                #     value="//div[@class='detail-product-title']/a[contains(@href,'product') and @class='inherit-class']",
                # ):
                #     count += 1
                #     # product_elements.append(element)
                #     print(f"element.text = '{element.text}'")


                results.append(temp_result)

        return results
    
    # @staticmethod
    # def _get_common_data(product: BeautifulSoup) -> dict:
    #     return {
    #         "UTCTime":      datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S"),
    #         "Retailer":     "PCCG",
    #         "Title":        product.find_next("a", class_="product-title").string,
    #         "URL":          product.find_next("a", class_="product-title").attrs["href"],
    #         "PriceAUD":     int(product.find_next("div", class_="price").string.strip("$")),
    #     }

    # @staticmethod
    # def _extract_ssd_data():
    def _extract_hdd_data(self, bs4_html_parser_list: list) -> list:
        results = []

        for bs4_html_parser in bs4_html_parser_list:
            for product in bs4_html_parser.find_all():
                # temp_result = self._get_common_data(product)
                temp_result = {}
                
                # print(f"==> Extracting data from '{???}'")

                # ### Print product URLs
                # count = 0
                # for element in driver.find_elements(
                #     by=By.XPATH,
                #     value="//div[@class='detail-product-title']/a[contains(@href,'product') and @class='inherit-class']",
                # ):
                #     count += 1
                #     # product_elements.append(element)
                #     print(f"element.text = '{element.text}'")


                results.append(temp_result)

        return results
