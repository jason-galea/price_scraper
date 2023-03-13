#!/usr/bin/python3

import os
import datetime
import enum
import json

from bs4 import BeautifulSoup as bs
# from selenium import webdriver
from selenium.webdriver import Firefox, DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from lib.common import *


class Scorptec:
    CATEGORY_URLS = {
        "hdd": "https://www.scorptec.com.au/product/hard-drives-&-ssds/hdd-3.5-drives",
        "ssd": "https://www.scorptec.com.au/product/hard-drives-&-ssds/solid-state-drives-ssd",
        "cpu": "",
        "gpu": "",
    },

    def __init__(self, category, output_dir, output_file, debug=False) -> None:


        ### TODO: Move this block into base class/common function
        #####################################################################
        ### Options
        ff_opts = Options()
        ff_opts.add_argument('-headless')
        ff_cap = DesiredCapabilities.FIREFOX
        ff_cap["marionette"] = True

        driver = Firefox(
            options=ff_opts,
            capabilities=ff_cap,
        )

        ### Request page
        driver.get(self.CATEGORY_URLS[category])
        #####################################################################


        ### Pagination fun!!!1!!!!!
        page_size_dropdown = Select(driver.find_element(By.ID, "pagination-view-count"))
        page_size_dropdown.select_by_visible_text("90")

        while (
            driver.find_element(By.ID, "current-page").text
            != driver.find_element(By.ID, "total-page").text
        ):
            for element in driver.find_elements(By.CLASS_NAME, "detail-product-title"):
                print(element.get_attribute("href"))

            driver.find_element(By.CLASS_NAME, "icomoon icomoon-chevron-right").click()

        exit(1)

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
    def _extract(self, category, bs4_html_parser: bs) -> list:
        match category:
            case "hdd":
                return self._extract_hdd_data(bs4_html_parser)
            case "ssd":
                return self._extract_ssd_data(bs4_html_parser)

    @staticmethod
    def _extract_hdd_data(): pass

    @staticmethod
    def _extract_ssd_data(): pass
