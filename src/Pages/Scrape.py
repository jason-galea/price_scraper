import datetime
import threading

from src.PCCG import PCCG
from src.Scorptec import Scorptec
from src.CentreCom import CentreCom

class Scrape:
    def start_extract_thread(self, website, category) -> None:

        ### TODO: Check if another thread is already running
        # if (???):
        #     print(f"\n==> ERROR: Another thread is already running, please wait a moment for it to finish")
        #     return

        NOW = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
        # JSON_OUTPUT_FILE = f"{JSON_OUTPUT_DIR}/{NOW}_{website}_{category}.json"

        match website:
            case "pccg": website_class = PCCG
            case "scorptec": website_class = Scorptec
            case "centrecom": website_class = CentreCom

        # print(f"\n==> INFO: Scraping with website '{website}' and category '{category}'")
        scrape_thread = threading.Thread(
            target=website_class,
            # args=(category, JSON_OUTPUT_DIR, JSON_OUTPUT_FILE),
            args=(category),
        )

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
