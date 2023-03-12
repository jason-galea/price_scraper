#!/usr/bin/python3

from bs4 import BeautifulSoup as bs
# from selenium import webdriver
from selenium.webdriver import Firefox, DesiredCapabilities
from selenium.webdriver.firefox.options import Options


def get_BS4_HTML_from_URL(url):

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
