#!/usr/bin/python3

### Imports
# import time
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

### Chrome imports
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions

### Firefox imports
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions


### I hate myself for using OOP
# def execute_with_retry(method, max_attempts):
#     e = None
#     for i in range(0, max_attempts):
#         try:
#             return method()
#         except Exception as e:
#             print(e)
#             time.sleep(1)
#     if e is not None:
#         raise e



### Static Class
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
    def GetPageChrome(site, category):
        ### Options
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--incognito')
        # chrome_options.add_argument('--headless')
        chrome_options.headless = True
        # https://stackoverflow.com/questions/53902507/unknown-error-session-deleted-because-of-page-crash-from-unknown-error-cannot
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")

        ### Service path
        chrome_service = Service("/usr/bin/chromedriver")

        ### Launch
        driver = webdriver.Chrome(
            service=chrome_service,
            options=chrome_options,
        )
        # driver.implicitly_wait(1)
        print("Success: Launched webdriver for Chrome")

        # TODO: Use a match/case statement here to compare user inputs & handle unknown input
        driver.get(Web.URLs[str(site).lower()][str(category).lower()])
        print("Success: Fetched HTML content of {}".format(driver.current_url))

        # Parse HTML content and return BS object
        return bs(driver.page_source, "html.parser")

    @staticmethod
    def GetPageFirefox(site, category):
        ### Sanitise input
        site = str(site).lower()
        category = str(category).lower()

        ### Options
        ff_opts = FirefoxOptions()
        # ff_opts.headless = True # Error: 'Options' object has no attribute 'binary'
        ff_opts.add_argument('-headless')
        ff_cap = DesiredCapabilities.FIREFOX
        ff_cap["marionette"] = True
        ff_bin = "/usr/bin/firefox"

        ### Launch
        # driver = execute_with_retry(
        #     lambda: webdriver.Firefox(
        #         # options=ff_opts,
        #         firefox_binary=ff_bin,
        #         capabilities=ff_cap,
        #     ),
        #     10
        # )
        driver = webdriver.Firefox(
            options=ff_opts,
            firefox_binary=ff_bin,
            capabilities=ff_cap,
        )
        # time.sleep(10)
        # print("Success: Launched webdriver for Chrome")

        ### TODO: Handle CLI options with match/case statement
        # print(Web.URLs[site][category])

        ### Request page
        driver.get(Web.URLs[site][category])

        ### Return BS object, containing parsed HTML
        return bs(driver.page_source, "html.parser")