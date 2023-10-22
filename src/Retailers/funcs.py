import datetime

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from flask_sqlalchemy import SQLAlchemy

import app ### app.py


### TODO: Start FF globally, reuse class to avoid MEM spikes
def create_webdriver() -> webdriver.Firefox:
    """
    Launches new webdriver
    """
    
    ff_opts = FirefoxOptions()
    ff_opts.add_argument('-headless')
    # ff_cap = DesiredCapabilities.FIREFOX
    # ff_cap["marionette"] = True
    # ff_opts.set_capability("marionette", True)

    return webdriver.Firefox(
        service=Service(executable_path="/usr/local/bin/geckodriver"),
        options=ff_opts,
        # capabilities=ff_cap,
    )


def concat_items_in_list(input_list: list, start_index: int, end_index: int) -> list:
    """
    Receives list & two indexes.\n
    Returns list with elements between the indexes concaternated (inclusive).\n
    E.G: concat_items_in_list(["a", "b", "c", "d"], 1, 2) --> ["a", "b c", "d"]
    """
    result_list = input_list
    for _ in range(end_index - start_index):
        result_list[start_index] = f"{input_list[start_index]} {input_list[start_index + 1]}"
        del result_list[start_index + 1]

    return result_list


def remove_strings_from_list(l: list, strings_to_remove: list) -> list:
    return [ s for s in l if (s not in strings_to_remove) ]


# def export_json(extracted_data: iter, dir: str, file: str) -> None:
#     print(f"==> INFO: Exporting data to '{file}'")

#     ### Check/Create dir
#     if not os.path.exists(dir):
#         os.makedirs(dir)

#     ### Write
#     with open(file, "w") as f:
#         f.write(json.dumps(extracted_data))


def export_to_db(db: SQLAlchemy, extracted_data: list) -> None:
    print("==> INFO: Entered 'export_to_db()'")
    print(f"==> DEBUG: extracted_data[0] = {extracted_data[0]}")

    for product_data in extracted_data:

        ### 
        # scraper  | ==> INFO: Scraping with website 'pccg' and category 'ssd'
        # scraper  | ==> INFO: Launching thread to scrape 'ssd' data from 'pccg'
        # scraper  | 172.21.0.1 - - [22/Oct/2023 13:39:04] "POST /scrape HTTP/1.1" 200 -
        # scraper  | ==> INFO: Entered 'export_to_db()'
        # scraper  | ==> DEBUG: extracted_data[0] = {'UTCTime': '2023-10-22T13:39:13.231445', 'Retailer': 'PCCG', 'Title': 'Samsung 870 EVO 2.5in SATA SSD 1TB', 'URL': 'https://www.pccasegear.com/products/53095/samsung-870-evo-2-5in-sata-ssd-1tb', 'PriceAUD': 129, 'FormFactor': '2.5in', 'Protocol': 'SATA', 'Brand': 'Samsung', 'CapacityGB': 1000, 'CapacityTB': 1.0, 'PricePerGB': 0.13, 'PricePerTB': 129.0}

        ### New entry
        temp_product = app.Product(
            utctime=product_data["UTCTime"]
        )

        ### Write entry to DB queue
        db.session.add(temp_product)

    ### Flush DB queue
    db.session.commit()


def get_utcnow_iso_8601() -> str:
    """
    Get current UTC time in ISO 8601 standard format
    """
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
