#!/usr/bin/python3

import os
import datetime
import enum
import json

from bs4 import BeautifulSoup as bs
# from selenium import webdriver
from selenium.webdriver import Firefox, DesiredCapabilities
from selenium.webdriver.firefox.options import Options

from lib.common import *


class CentreCom:
    URLS = {
        "hdd": "",
        "ssd": "",
        "cpu": "",
        "gpu": "",
    },

    def __init__(self, category) -> None:
        self.category = category

    def begin(): pass
        
    def _download_html(): pass

    def _extract_hdd_data(): pass

    def _extract_sdd_data(): pass

