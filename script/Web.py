#!/usr/bin/python3

### Imports
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs


class Web:
    URLs = {
        "pccg": {
            "hdd": "https://www.pccasegear.com/category/210_344/hard-drives-ssds/3-5-hard-drives"
            , "ssd": ""
            , "cpu": ""
            , "gpu": ""
        }
        , "scorptec" : {
            "hdd": ""
            , "ssd": ""
            , "cpu": ""
            , "gpu": ""
        }
        # etc...
    }

    @staticmethod
    def GetPage(site, category):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--headless')
        # https://stackoverflow.com/questions/53902507/unknown-error-session-deleted-because-of-page-crash-from-unknown-error-cannot
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        # driver.implicitly_wait(1)

        # TODO: Use a match/case statement here to compare user inputs & handle unknown input
        driver.get(Web.URLs[str(site).lower()][str(category).lower()])

        # Parse HTML content and return BS object
        return bs(driver.page_source, "html.parser")