#!/usr/bin/python3

# import time
from optparse import Option
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox.options import Options



class Web:
    # This is only meant to fetch a single page at a time, for now.
    # If I need to fetch multiple pages, or navigate between pages, I'll split this up a lot more.

    URLs = {
        "pccg": {
            "hdd": "https://www.pccasegear.com/category/210_344/hard-drives-ssds/3-5-hard-drives",
            "ssd": "",
            "cpu": "",
            "gpu": "",
        },
        "scorptec": {
            "hdd": "",
            "ssd": "",
            "cpu": "",
            "gpu": "",
        },
        # etc...
    }

    @staticmethod
    def GetPage(site, category):
        ### Sanitise input
        site = str(site).lower()
        category = str(category).lower()

        ### Options
        ff_opts = Options()
        ff_opts.add_argument('-headless')
        ff_cap = DesiredCapabilities.FIREFOX
        ff_cap["marionette"] = True

        driver = webdriver.Firefox(
            options=ff_opts,
            capabilities=ff_cap,
        )

        ### TODO: Handle CLI options with match/case statement
        # print(Web.URLs[site][category])

        ### Request page
        driver.get(Web.URLs[site][category])

        ### Return BS object, containing parsed HTML
        return bs(driver.page_source, "html.parser")