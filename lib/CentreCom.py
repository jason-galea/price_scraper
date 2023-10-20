class CentreCom:
    pass

# import os
# import datetime
# import enum
# import json
# from bs4 import BeautifulSoup as bs
# from selenium import webdriver
# from selenium.webdriver import DesiredCapabilities
# # from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select

# from common import *


# class CentreCom:
#     URLS = {
#         "hdd": "",
#         "ssd": "",
#         "cpu": "",
#         "gpu": "",
#     },

#     def __init__(self, category) -> None:
#         self.category = category

#     def download_html(self, url="") -> bs:

#         ### Workaround for not being able to use "self.var" as default value
#         if (url == ""):
#             url = self.URLS[self.category]

#         ### Options
#         ff_opts = Options()
#         ff_opts.add_argument('-headless')
#         ff_cap = DesiredCapabilities.FIREFOX
#         ff_cap["marionette"] = True

#         driver = webdriver.Firefox(
#         # driver = Firefox(
#             options=ff_opts,
#             capabilities=ff_cap,
#         )

#         ### Request page
#         driver.get(url)

#         ### Return BS object, containing parsed HTML
#         return bs(
#             markup=driver.page_source,
#             features="html.parser"
#         )

#     def extract(self, bs4_html_parser: bs) -> list:
#         match self.category:
#             case "hdd":
#                 return self._extract_hdd_data(bs4_html_parser)
#             case "ssd":
#                 return self._extract_ssd_data(bs4_html_parser)

#     def _extract_hdd_data(): pass

#     def _extract_ssd_data(): pass

