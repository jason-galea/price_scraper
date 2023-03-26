import os
# import datetime
# import enum
import json
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver import Firefox, DesiredCapabilities
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lib.common import *


class Scorptec:
    CATEGORY_URLS = {
        "hdd": "https://www.scorptec.com.au/product/hard-drives-&-ssds/hdd-3.5-drives",
        "ssd": "https://www.scorptec.com.au/product/hard-drives-&-ssds/solid-state-drives-ssd",
        # "cpu": "",
        # "gpu": "",
    }

    def __init__(self, category, output_dir, output_file, debug=False) -> None:
        ### Download URL
        driver = instantiate_ff_driver_and_download(self.CATEGORY_URLS[category])

        ### Pagination fun!!!1!!!!
        ### 90 items per page
        # select_dropdown = Select(driver.find_element(By.ID, "pagination-view-count"))
        # select_dropdown.select_by_visible_text("90")
        
        # ### Sort by price, low to high
        # sort_dropdown = Select(driver.find_element(By.ID, "widget-sort"))
        # sort_dropdown.select_by_visible_text("Price (low to high)")

        last_page = int(driver.find_element(By.ID, "total-page").text)
        # last_page = None
        # product_elements = []
        bs4_hmtl_parsers = []

        ### TODO: Refactor so pages are fetched within the iteration they are parsed
        while True:
            # ### First iteration, find last_page and skip repeat download
            # if (not last_page):
            #     last_page = int(driver.find_element(By.ID, "total-page").text)
            # else:

            ### Find current page
            # print(f"==> INFO: Attempting to find current page")
            current_page_element = WebDriverWait(driver, 10).until(
                lambda x: x.find_element(By.ID, "current-page")
            )
            current_page = int(current_page_element.text)
            # current_page = int(driver.find_element(By.ID, "current-page").text)
            print(f"==> INFO: Opened page {current_page}/{last_page}")

            ### Print product URLs
            count = 0
            for element in driver.find_elements(
                by=By.XPATH,
                value="//div[@class='detail-product-title']/a[contains(@href,'product') and @class='inherit-class']",
            ):
                count += 1
                # product_elements.append(element)
                print(f"element.text = '{element.text}'")
            print(f"==> INFO: Found {count} products on page {current_page}/{last_page}")

            ### Save HTML parser objects
            bs4_hmtl_parsers.append(
                BeautifulSoup(
                    markup=driver.page_source,
                    features="html.parser"
                )
            )

            ### Go to next page (somehow)
            # if (current_page < int(last_page) - 1):
            if (current_page != last_page):
                # print(f"==> INFO: Attempting to load {self.CATEGORY_URLS[category]}?page={current_page + 1}")
                
                # driver.close() ### Workaround for anti-bot nonsense
                driver.delete_all_cookies() ### Workaround for anti-bot nonsense
                next_page_url = f"{self.CATEGORY_URLS[category]}?page={current_page + 1}"
                # driver = instantiate_ff_driver_and_download(next_page_url)
                driver.get(next_page_url)
            else:
                # print(f"==> INFO: Found a total of {len(product_elements)} product elements")
                break

        return

        ### Create HTML parser
        bs4_html_parser = bs(
            markup=driver.page_source,
            features="html.parser"
        )

        ### Extract
        extracted_data = self._extract(category, bs4_html_parser)

        ### Debug
        if (debug):
            print(json.dumps(extracted_data, indent=4))

        ### Export
        export_json(extracted_data, output_dir, output_file)

        ### Cleanup
        os.system('pkill firefox') ### Lol. Lmao


    ### TODO: Move this into base class/common function
    def _extract(self, category, bs4_html_parser: BeautifulSoup) -> list:
        match category:
            case "hdd":
                return self._extract_hdd_data(bs4_html_parser)
            case "ssd":
                return self._extract_ssd_data(bs4_html_parser)

    @staticmethod
    def _extract_hdd_data(): pass

    @staticmethod
    def _extract_ssd_data(): pass
