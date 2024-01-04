import re
import json

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup, PageElement

from src.Database import CATEGORY_CLASS_DICT
from src.generic_funcs import get_utcnow_iso_8601
from src.Retailers.funcs import create_webdriver, concat_items_in_list


class PCCG:
    """
    TODO: docstring
    """

    CATEGORY_URLS = {
        "hdd": "https://www.pccasegear.com/category/210_344/hard-drives-ssds/3-5-hard-drives",
        "ssd": "https://www.pccasegear.com/category/210_902/hard-drives-ssds/solid-state-drives-ssd",
        "ddr4": "https://www.pccasegear.com/category/186_1782/memory/all-ddr4-memory",
        "ddr5": "https://www.pccasegear.com/category/186_2181/memory/all-ddr5-memory",
        # "cpu": "",
        # "gpu": "",
    }
    COMMON_SSD_CATEGORY_MAPPINGS = {
        "FormFactor":{
            "2.5in":    "2.5in",
            "2.5inch":  "2.5in",
            "2.5-inch": "2.5in",
            "M.2":      "M.2",
            "NVMe":     "M.2",
            "NVME":     "M.2",
        },
        "Protocol":{
            "SATA":     "SATA",
            "2.5in":    "SATA",
            "2.5inch":  "SATA",
            "4.0":      "NVMe Gen4",
            "Gen4":     "NVMe Gen4",
            "Gen4x4":   "NVMe Gen4",
            "NVMe":     "NVMe Gen3", ### NOTE: Assume "NVMe" = PCIe Gen3, since we already found all Gen4 drives
            "NVME":     "NVMe Gen3",
            "Gen3x4":   "NVMe Gen3",
        },
        "Brand":{
            "ASUS":     "ASUS",
            "Samsung":  "Samsung",
            "ADATA":    "ADATA",
            "Corsair":  "Corsair",
            "Crucial":  "Crucial",
            "Kingston": "Kingston",
            "MSI":      "MSI",
            "Team":     "Team",
            "Western":  "Western Digital",
            "Gigabyte": "Gigabyte",
            "PNY":      "PNY",
            "Seagate":  "Seagate",
        }
    }
    # RAM_REGEX_PATTERN = r"(^[a-zA-Z\.]+) ([a-zA-Z\-\ 5]*)(\d+)GB \(((\d)x(\d+)GB)\) (\d{4}[MHhz]{3}) (CL\d{2}) +(DDR\d)(.*)"
    RAM_REGEX_PATTERN = r"(^[a-zA-Z\.]+) ([a-zA-Z\-\ 5]*)(\d+)GB \(((\d)x(\d+)GB)\) (\d{4}[MHhz]{3}) (CL\d{2}) +DDR\d(.*)"

    def __init__(self, app: Flask, category: str, _debug=False) -> None:

        base_url = self.CATEGORY_URLS[category]

        driver = create_webdriver()
        driver.get(base_url)

        ### Create HTML parser
        bs4_html_parser = BeautifulSoup(
            markup=driver.page_source,
            features="html.parser"
        )

        bs4_products = bs4_html_parser.find_all("div", class_="product-container")
        current_utctime = get_utcnow_iso_8601()

        match category:
            case "hdd":
                extracted_data = self._extract_hdd_data(bs4_html_parser, current_utctime)
            case "ssd":
                extracted_data = [
                    d for product in bs4_products
                    if (d := self._extract_ssd_data(product, current_utctime))
                ]
            case "ddr4" | "ddr5":
                extracted_data = [
                    d for product in bs4_products
                    if (d := self._extract_ram_data(product, current_utctime))
                ]

        # if debug:
        #     print(json.dumps(extracted_data, indent=4))
        print(f"==> DEBUG: extracted_data[0] = {json.dumps(extracted_data[0], indent=4)}")

        ### Write to DB
        with app.app_context():
            # export_to_db(db, extracted_data)
            CATEGORY_CLASS_DICT[category].export_to_db(extracted_data)

        driver.quit()


    @staticmethod
    def _get_common_data(product: BeautifulSoup, current_utctime: str) -> dict:
        return {
            "UTCTime":      current_utctime,
            "Retailer":     "pccg", ### Must match `config.py`
            "Title":        product.find_next("a", class_="product-title").string,
            "URL":          product.find_next("a", class_="product-title").attrs["href"],
            "PriceAUD":     int(product.find_next("div", class_="price").string.strip("$")),
        }


    @staticmethod
    def _extract_hdd_data(bs4_html_parser: BeautifulSoup, current_utctime: str) -> list:

        results = []

        for product in bs4_html_parser.find_all("div", class_="product-container"):


            ########################################################################################
            ### NON-WEBSITE, NON-CATEGORY SPECIFIC DATA
            ### TODO: Move these into a common function

            ### Setup & data common to PCCG
            result = PCCG._get_common_data(product, current_utctime)
            # result.update({"Category": "hdd"})

            ### TODO: Fetch full description from current products "url"
            # description_soup = Web.get_bs4_html_parser_from_URL(result["URL"])
            # result.update({
            #     # "Description":description_soup.find_next("div", id_="overview").string
            #     # "Description":description_soup.find_next("div", class_="tab-pane").string
            #     "Description":description_soup.find_next("div", class_="tab-pane")
            #     # "Description":description_soup.select_one("div.tab-pane.active")
            # })

            ### TODO: Extract even more data from description?
            ### Lots of caveats, as desciption varies enormously
            # description_a = description.split()

            title_split: list = result["Title"].split()
            # print(["Brand", "Series", "ModelNumber", "FormFactor", "Protocol", "Capacity"])
            # print(title_split)


            ### Discard unwanted items
            if "Upgrade" in title_split:
                continue


            ########################################################################################
            ### WEBSITE & CATEGORY SPECIFIC DATA

            ### Remove unneeded words
            if "WD" in title_split:
                title_split.remove("WD")

            ### Make array consistent to Brand/Series/Model
            if title_split[0] == "Western": # ["Western", "Digital", "WD"] --> ["Western Digital"]
                title_split = concat_items_in_list(title_split, 0, 1)

                if (title_split[1] == "Red") and (title_split[2] in ["Plus", "Pro"]):
                    title_split = concat_items_in_list(title_split, 1, 2)

            # print(title_split)

            ### Preprocess common values
            capacity_gb = int(title_split[2].strip("TB"))*1000
            capacity_tb = round(capacity_gb/1000, 2)

            ### Save
            result.update({
                "Brand": title_split[0],
                "Series": title_split[1],
                "HDDModel": title_split[3],
                "CapacityGB": float(capacity_gb),
                "PricePerGB": float(round(result["PriceAUD"]/capacity_gb, 2)),
                "CapacityTB": float(capacity_tb),
                "PricePerTB": float(round(result["PriceAUD"]/capacity_tb, 2)),
            })

            ########################################################################################

            results.append(result)

        return results


    @staticmethod
    def _extract_ssd_data(product: PageElement, current_utctime: str) -> dict:

        ############################################################################################
        ### NON-WEBSITE, NON-CATEGORY SPECIFIC DATA
        result = PCCG._get_common_data(product, current_utctime)

        title_split = result["Title"].split()
        # print(["Brand", "Series", "ModelNumber", "FormFactor", "Protocol", "Capacity"])
        # print(title_split)

        ### Discard unwanted items
        if (
            ("Upgrade" in title_split)
            or ("Western Digital G-D" in result["Title"])
        ): return


        ############################################################################################
        ### WEBSITE & CATEGORY SPECIFIC DATA

        ### Common 1:1 matches
        ### TODO: Use REGEX instead?
        ### TODO: MY GOD PLEASE USE REGEX, THIS IS RIDICULOUS
        for d_categories, category_mappings in PCCG.COMMON_SSD_CATEGORY_MAPPINGS.items():
            for matching_string, value in category_mappings.items():
                if (matching_string in title_split):
                    result.update({ d_categories:value })
                    break

            if (d_categories not in result.keys()):
                print(f"==> WARN: {d_categories} not found in title: {title_split}")

        ### "CapacityGB", "PricePerGB", "PricePerGB"
        capacity_dict = {
            "TB":1000,
            "GB":1,
        }
        for label, val in capacity_dict.items():
            for s in reversed(title_split):
                if (label in s) and (s != "RGB"): ### E.G: "TB" in "10TB"
                    capacity_gb = int( s.strip(label) )*val ### E.G: 10*1000
                    result.update({
                        "CapacityGB": float(capacity_gb),
                        "CapacityTB": float(round( capacity_gb/1000, 2 )),
                        "PricePerGB": float(round( result["PriceAUD"]/capacity_gb, 2 )),
                        "PricePerTB": float(round( result["PriceAUD"]/(capacity_gb/1000), 2 )),
                    })

        if ("CapacityGB" not in result.keys()):
            print(f"==> WARN: CapacityGB not found in title: {title_split}")

        return result


    @staticmethod
    def _extract_ram_data(product: PageElement, current_utctime: str) -> dict:

        ############################################################################################
        ### COMMON FIELDS
        temp_result = PCCG._get_common_data(product, current_utctime)
        # temp_result.update({"Category": category})

        ### Handle REALLY specific errors
        if (temp_result["Title"] == 'Corsair Vengeance 48GB (2x24GB) 7000MHz C40 DDR5'): ### "C40"
            temp_result["Title"] = 'Corsair Vengeance 48GB (2x24GB) 7000MHz CL40 DDR5'
        if (temp_result["Title"] == 'Team T-Force Delta RGB 64GB (2x32GB) 5200MHz CL40 Black'): ### Missing "DDR5"
            temp_result["Title"] = 'Team T-Force Delta RGB 64GB (2x32GB) 5200MHz CL40 DDR5 Black'

        title = temp_result["Title"]


        ############################################################################################
        ### STATIC FIELDS

        regex_result = re.search(
            pattern=PCCG.RAM_REGEX_PATTERN,
            string=title,
        )

        if not regex_result:
            print(f"==> WARN: REGEX failed on title: '{title}'")
            return ### This "None" must be removed from list comprehension in "_extract()"

        ### Create dict from capture group results
        ### NOTE: Need to associate keys & values before removing anything
        regex_groups_keys = [
            "Brand", "RAMModel", "RAMCapacityGB", "KitConfiguration",
            "SticksPerKit", "CapacityPerStick", "Clock", "CASPrimary", "Misc"
        ]
        ### Strip spaces
        regex_groups_vals = [ val.strip() for val in regex_result.groups() ]
        ### Convert ints to ints
        regex_groups_vals = [ (int(s) if (s.isdigit()) else s) for s in regex_groups_vals ]

        # print(f"==> INFO: regex_groups_keys = {regex_groups_keys}")
        # print(f"==> INFO: regex_groups_vals = {regex_groups_vals}")
        # break
        regex_groups_dict = dict(zip( regex_groups_keys, regex_groups_vals ))


        ### TODO: Figure out if this is still needed?
        # ### TODO: Handle wierd cases
        # if (regex_groups_dict["Misc"] == "White"):
        #     pass
        # if (regex_groups_dict["RAMModel"] == ""):
        #     pass

        # print(f"==> INFO: regex_groups_dict = {json.dumps(regex_groups_dict, indent=4)}")
        temp_result.update(regex_groups_dict)


        ############################################################################################
        ### CALCULATED FIELDS
        temp_result.update({
            ### NOTE: Assumption based on PCCG UI, there are only two possible values
            ### NOTE: "Lighting" allows for other values from different retailers, such as "White"
            "Lighting": "RGB" if re.search(r"RGB", title) else "No lighting",
            "RAMFormFactor": "SODIMM" if re.search(r"SODIMM", title) else "DIMM",
            "RAMPricePerGB": round( temp_result["PriceAUD"] / temp_result["RAMCapacityGB"], 2 ),
        })


        ### DEBUGGING
        # del temp_result["Misc"]
        # del temp_result["Lighting"]

        # if (temp_result == null):


        ############################################################################################
        ### Add individual product data to results
        # print(f"==> INFO: temp_result = {json.dumps(temp_result, indent=4)}")
        # break
        # results.append(temp_result)
        return temp_result
