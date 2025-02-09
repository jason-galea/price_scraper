# import datetime
import threading
# import debugpy

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

from src.Retailers.PCCG import PCCG
from src.Retailers.Scorptec import Scorptec
from src.Retailers.CentreCom import CentreCom

class Scrape:
    """
    Container class for methods related to the "Scrape" page
    """

    @staticmethod
    def start_extract_thread(app: Flask, website: str, category: str) -> None:
        """
        Starts a new thread to avoid the page "freezing" when submitting forms.

        Each thread will:
        - Download web page
        - Extract useful data
        - Save data to database
        """

        # print(f"==> DEBUG: start_extract_thread(): website = {website}")
        # print(f"==> DEBUG: start_extract_thread(): category = {category}")

        match website:
            case "pccg": website_class = PCCG
            case "scorptec": website_class = Scorptec
            case "centrecom": website_class = CentreCom

        # print(f"\n==> INFO: Scraping with website '{website}' and category '{category}'")
        scrape_thread = threading.Thread(
            target=website_class,
            args=(app, category,), ### NOTE: COMMA IS REQUIRED LOL
        )

        # debugpy.breakpoint()

        print(f"==> INFO: Launching thread to scrape '{category}' data from '{website}'")
        scrape_thread.start()

        # while True:
        #     try:
        #         scrape_thread.start()
        #         break
        #     except WebDriverException as e:
        #         print(f"\n==> WARN: WebDriverException exception raised: '{e}'")
        #         print(f"\n==> WARN: This was most likely caused by conflicting threads")
        #         print(f"\n==> WARN: Restarting thread")
        #         continue
