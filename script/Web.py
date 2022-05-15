#!/usr/bin/python3

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Firefox
from selenium.webdriver.firefox.options import Options


class Web:
    ### This is only meant to fetch a single page at a time, for now.
    ### If I need to fetch multiple pages, or navigate between pages, I'll split this up a lot more.

    @staticmethod
    def GetPageSoup(url):

        ### Options
        ff_opts = Options()
        ff_opts.add_argument('-headless')
        ff_cap = DesiredCapabilities.FIREFOX
        ff_cap["marionette"] = True

        # driver = webdriver.Firefox(
        driver = Firefox(
            options=ff_opts,
            capabilities=ff_cap,
        )

        ### Request page
        driver.get(url)

        ### Return BS object, containing parsed HTML
        return bs(driver.page_source, "html.parser")