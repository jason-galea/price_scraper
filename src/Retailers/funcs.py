# import datetime
# import json

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from flask_sqlalchemy import SQLAlchemy

# from app import Product ### Circular import?
# import app
# from src.Database.Product import Product
from src.config import CATEGORY_CLASS_DICT


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


# def export_to_db(db: SQLAlchemy, extracted_data: list) -> None:
#     print("==> DEBUG: Entered 'export_to_db()'")
#     # print(f"==> DEBUG: extracted_data[0] = {json.dumps(extracted_data[0], indent=4)}")

#     # scraper  | ==> DEBUG: extracted_data[0] = {
#     # scraper  |     "UTCTime": "2024-01-01T08:55:56.648311",
#     # scraper  |     "Retailer": "PCCG",
#     # scraper  |     "Title": "Samsung 870 EVO 2.5in SATA SSD 1TB",
#     # scraper  |     "URL": "https://www.pccasegear.com/products/53095/samsung-870-evo-2-5in-sata-ssd-1tb",
#     # scraper  |     "PriceAUD": 165,
#     # scraper  |     "Category": "ssd",

#     # scraper  |     "FormFactor": "2.5in",
#     # scraper  |     "Protocol": "SATA",
#     # scraper  |     "Brand": "Samsung",
#     # scraper  |     "CapacityGB": 1000,
#     # scraper  |     "CapacityTB": 1.0,
#     # scraper  |     "PricePerGB": 0.17,
#     # scraper  |     "PricePerTB": 165.0
#     # scraper  | }

#     # category_class = CATEGORY_CLASS_DICT[category]
#     # category_class = Product

#     for product_data in extracted_data:
#         # print(f"==> DEBUG: product_data = {json.dumps(product_data, indent=4)}")

#         temp_product = category_class(
#             title=product_data["Title"],
#             retailer=product_data["Retailer"],
#             utctime=product_data["UTCTime"],
#             # category=product_data["Category"],
#         )

#         ### Write entry to DB queue
#         db.session.add(temp_product)

#     ### Flush DB queue
#     print("==> DEBUG: Flushing DB queue")
#     db.session.commit()

#     print("==> DEBUG: Exiting 'export_to_db()' successfully?? :oooo")
