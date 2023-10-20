# import os
import re
import datetime
# import enum
import json
from bs4 import BeautifulSoup, PageElement
# from selenium import webdriver
# from selenium.webdriver import Firefox, DesiredCapabilities
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select

from lib.common import *

class PCCG:
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

    def __init__(self, category, output_dir, output_file, debug=False) -> None:

        driver = instantiate_ff_driver_and_download(self.CATEGORY_URLS[category])

        ### Create HTML parser
        bs4_html_parser = BeautifulSoup(
            markup=driver.page_source,
            features="html.parser"
        )

        extracted_data = self._extract(category, bs4_html_parser)

        if (debug):
            print(json.dumps(extracted_data, indent=4))

        export_json(extracted_data, output_dir, output_file)

    ### TODO: Move this into base class/common function
    def _extract(self, category: str, bs4_html_parser: BeautifulSoup) -> list:
        bs4_products = bs4_html_parser.find_all("div", class_="product-container")

        match category:
            case "hdd":
                return self._extract_hdd_data(bs4_html_parser)
            case "ssd":
                # return [ self._extract_ssd_data(product) for product in bs4_products ]
                return [ d for product in bs4_products if (d := self._extract_ssd_data(product)) is not None ]
            case "ddr4" | "ddr5":
                return [ d for product in bs4_products if (d := self._extract_ram_data(product)) is not None ]

    @staticmethod
    def _get_common_data(product: BeautifulSoup) -> dict:
        return {
            "UTCTime":      datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S"),
            "Retailer":     "PCCG",
            "Title":        product.find_next("a", class_="product-title").string,
            "URL":          product.find_next("a", class_="product-title").attrs["href"],
            "PriceAUD":     int(product.find_next("div", class_="price").string.strip("$")),
        }

    @staticmethod
    def _extract_hdd_data(bs4_html_parser: BeautifulSoup) -> list:
    
        results = []

        for product in bs4_html_parser.find_all("div", class_="product-container"):


            #############################################################################################
            ### NON-WEBSITE, NON-CATEGORY SPECIFIC DATA
            ### TODO: Move these into a common function

            ### Setup & data common to PCCG
            result = PCCG._get_common_data(product)

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

            title_split = result["Title"].split()
            # print(["Brand", "Series", "ModelNumber", "FormFactor", "Protocol", "Capacity"])
            # print(title_split)


            ### Discard unwanted items
            if ("Upgrade" in title_split): continue


            #############################################################################################
            ### WEBSITE & CATEGORY SPECIFIC DATA
            
            ### Remove unneeded words
            title_split = remove_multiple_strings_from_list(title_split, ["WD"])
            
            ### Make array consistent to Brand/Series/Model
            if title_split[0] == "Western": # ["Western", "Digital", "WD"] --> ["Western Digital"]
                title_split = concaternate_items_within_list(title_split, 0, 1)

                if (title_split[1] == "Red") and (title_split[2] in ["Plus", "Pro"]):
                    title_split = concaternate_items_within_list(title_split, 1, 2)

            # print(title_split)

            ### Preprocess common values
            capacity_gb = int(title_split[2].strip("TB"))*1000
            capacity_tb = round(capacity_gb/1000, 2)

            ### Save
            result.update({
                "Brand": title_split[0],
                "Series": title_split[1],
                "Model": title_split[3],
                # "CapacityRaw": title_split[2],
                "CapacityGB": capacity_gb,
                "PricePerGB": round(result["PriceAUD"]/capacity_gb, 2),
                "CapacityTB": capacity_tb,
                "PricePerTB": round(result["PriceAUD"]/capacity_tb, 2),
            })

            #############################################################################################

            results.append(result)

        return results

    @staticmethod
    def _extract_ssd_data(product: PageElement) -> dict:

        #############################################################################################
        ### NON-WEBSITE, NON-CATEGORY SPECIFIC DATA
        result = PCCG._get_common_data(product)

        title_split = result["Title"].split()
        # print(["Brand", "Series", "ModelNumber", "FormFactor", "Protocol", "Capacity"])
        # print(title_split)

        ### Discard unwanted items
        if (
            ("Upgrade" in title_split)
            or ("Western Digital G-D" in result["Title"])
        ): return


        #############################################################################################
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
                if (label in s) and (s != "RGB"):
                    capacity_gb = int( s.strip(label) )*val
                    result.update({
                        "CapacityGB":capacity_gb,
                        "CapacityTB":round( capacity_gb/1000, 2 ),
                        "PricePerGB":round( result["PriceAUD"]/capacity_gb, 2 ),
                        "PricePerTB":round( result["PriceAUD"]/(capacity_gb/1000), 2 ),
                    })
                    break

        if ("CapacityGB" not in result.keys()):
            print(f"==> WARN: CapacityGB not found in title: {title_split}")
        
        return result

    @staticmethod
    def _extract_ram_data(product: PageElement) -> dict:

        #############################################################################################
        ### COMMON FIELDS
        temp_result = PCCG._get_common_data(product)
        
        ### Handle REALLY specific errors        
        if (temp_result["Title"] == 'Corsair Vengeance 48GB (2x24GB) 7000MHz C40 DDR5'): ### "C40"
            temp_result["Title"] = 'Corsair Vengeance 48GB (2x24GB) 7000MHz CL40 DDR5'
        if (temp_result["Title"] == 'Team T-Force Delta RGB 64GB (2x32GB) 5200MHz CL40 Black'): ### Missing "DDR5"
            temp_result["Title"] = 'Team T-Force Delta RGB 64GB (2x32GB) 5200MHz CL40 DDR5 Black'

        title = temp_result["Title"]


        #############################################################################################
        ### STATIC FIELDS

        regex_result = re.search(
            pattern=r"(^[a-zA-Z\.]+) ([a-zA-Z\-\ 5]*)(\d+)GB \(((\d)x(\d+)GB)\) (\d{4}[MHhz]{3}) (CL\d{2}) +(DDR\d)(.*)",
            string=title,
        )

        if (not regex_result):
            print(f"==> WARN: REGEX failed on title: '{title}'")
            return ### This "None" needs to be filtered out of the list comprehension in "_extract()"

        ### Create dict from capture group results
        ### NOTE: Need to associate keys & values before removing anything
        regex_groups_keys = ["Brand", "Model", "CapacityGB", "KitConfiguration", "SticksPerKit", "CapacityPerStick", "Clock", "CASPrimary", "MemoryType", "Misc"]
        regex_groups_vals = [ val.strip() for val in regex_result.groups() ] ### Strip spaces
        regex_groups_vals = [ (int(s) if (s.isdigit()) else s) for s in regex_groups_vals ] ### Convert ints to ints
        
        # print(f"==> INFO: regex_groups_keys = {regex_groups_keys}")
        # print(f"==> INFO: regex_groups_vals = {regex_groups_vals}")
        # break
        regex_groups_dict = dict(zip( regex_groups_keys, regex_groups_vals ))


        ### TODO: Figure out if this is still needed?
        # ### TODO: Handle wierd cases
        # if (regex_groups_dict["Misc"] == "White"):
        #     pass
        # if (regex_groups_dict["Model"] == ""):
        #     pass

        # print(f"==> INFO: regex_groups_dict = {json.dumps(regex_groups_dict, indent=4)}")
        temp_result.update(regex_groups_dict)

        
        #############################################################################################
        ### CALCULATED FIELDS
        temp_result.update({
            ### NOTE: Assumption based on PCCG UI, there are only two possible values
            ### NOTE: "Lighting" allows for other values from different retailers, such as "White"
            "Lighting": "RGB" if ( re.search(r"RGB", title) != None ) else "No lighting",
            "FormFactor": "SODIMM" if ( re.search(r"SODIMM", title) != None ) else "DIMM",
            "PricePerGB": round( temp_result["PriceAUD"] / temp_result["CapacityGB"], 2 ),
        })


        ### DEBUGGING
        # del temp_result["Misc"]
        # del temp_result["Lighting"]

        # if (temp_result == null):





        #############################################################################################
        ### Add individual product data to results
        # print(f"==> INFO: temp_result = {json.dumps(temp_result, indent=4)}")
        # break
        # results.append(temp_result)
        return temp_result
