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

from lib.common import *


class Scorptec:
    CATEGORY_URLS = {
        "hdd": "",
        "ssd": "",
        "cpu": "",
        "gpu": "",
    },

    def __init__(self, category, output_dir, output_file, debug=False) -> None:

        url = self.CATEGORY_URLS[category]

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
        driver.get(url)

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


    ### TODO: Move this into a base class
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
