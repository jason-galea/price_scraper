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


class PCCG:
    CATEGORY_URLS = {
        "hdd": "https://www.pccasegear.com/category/210_344/hard-drives-ssds/3-5-hard-drives",
        "ssd": "https://www.pccasegear.com/category/210_902/hard-drives-ssds/solid-state-drives-ssd",
        # "cpu": "",
        # "gpu": "",
    }

    def __init__(self, category, output_dir, output_file, debug=False) -> None:

        ### TODO: Move this block into base class/common function
        #####################################################################
        ### Options
        ff_opts = Options()
        ff_opts.add_argument('-headless')
        ff_cap = DesiredCapabilities.FIREFOX
        ff_cap["marionette"] = True

        driver = Firefox(
            options=ff_opts,
            capabilities=ff_cap,
        )

        ### Request page
        driver.get(self.CATEGORY_URLS[category])
        #####################################################################


        ### Create HTML parser
        bs4_html_parser = bs(
            markup=driver.page_source,
            features="html.parser"
        )

        ### Extract
        extracted_data = self._extract(category, bs4_html_parser)

        ### Debug
        if (debug):
            print(json.dumps(extracted_data, indent=4))

        ### Export
        export_json(extracted_data, output_dir, output_file)

        ### Cleanup
        os.system('pkill firefox') ### Lol. Lmao


    ### TODO: Move this into base class/common function
    def _extract(self, category, bs4_html_parser: bs) -> list:
        match category:
            case "hdd":
                return self._extract_hdd_data(bs4_html_parser)
            case "ssd":
                return self._extract_ssd_data(bs4_html_parser)

    @staticmethod
    def _extract_hdd_data(bs4_html_parser: bs) -> list:
    
        results = []

        for product in bs4_html_parser.find_all("div", class_="product-container"):


            #############################################################################################
            ### NON-WEBSITE, NON-CATEGORY SPECIFIC DATA
            ### TODO: Move these into a common function

            ### Setup & data common to PCCG
            result = {
                "UTCTime":  datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S"),
                "Retailer": "PCCG",
                "Title":    product.find_next("a", class_="product-title").string,
                "URL":      product.find_next("a", class_="product-title").attrs["href"],
                "PriceAUD": int(product.find_next("div", class_="price").string.strip("$")),
            }

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
    def _extract_ssd_data(bs4_html_parser: bs) -> list:

        results = []
    
        for product in bs4_html_parser.find_all("div", class_="product-container"):


            #############################################################################################
            ### NON-WEBSITE, NON-CATEGORY SPECIFIC DATA
            ### TODO: Move these into a common function

            ### Setup & data common to PCCG
            result = {
                "UTCTime":  datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S"),
                "Retailer": "PCCG",
                "Title":    product.find_next("a", class_="product-title").string,
                "URL":      product.find_next("a", class_="product-title").attrs["href"],
                "PriceAUD": int(product.find_next("div", class_="price").string.strip("$")),
            }

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

            ### Common 1:1 matches
            ### "FormFactor", "Protocol", "Brand"
            ### TODO: Use REGEX instead?
            common_category_mappings = {
                "FormFactor":{
                    "2.5in":"2.5in",
                    "2.5inch":"2.5in",
                    "2.5-inch":"2.5in",
                    "M.2":"M.2",
                    "NVMe":"M.2",
                    "NVME":"M.2",
                },
                "Protocol":{
                    "SATA":"SATA",
                    "2.5inch":"SATA",
                    "Gen4":"NVMe Gen4",
                    "Gen4x4":"NVMe Gen4",
                    "NVMe":"NVMe Gen3", ### NOTE: Assume "NVMe" = PCIe Gen3, since we already found all Gen4 drives 
                    "NVME":"NVMe Gen3",
                },
                "Brand":{
                    "ASUS":"ASUS",
                    "Samsung":"Samsung",
                    "ADATA":"ADATA",
                    "Corsair":"Corsair",
                    "Crucial":"Crucial",
                    "Kingston":"Kingston",
                    "MSI":"MSI",
                    "Team":"Team",
                    "Western":"Western Digital",
                    "Gigabyte":"Gigabyte",
                }
            }

            for d_categories, category_mappings in common_category_mappings.items():
                for matching_string, value in category_mappings.items():
                    if (matching_string in title_split):
                        result.update({ d_categories:value })
                        break

                if (d_categories not in result.keys()):
                    print(f"{d_categories} not found in title: {title_split}")

            ### "CapacityGB", "PricePerGB", "PricePerGB"
            capacity_dict = {
                "TB":1000,
                "GB":1,
            }
            for label, val in capacity_dict.items():
                for s in reversed(title_split):
                    if (label in s):
                        capacity_gb = int(s.strip(label))*val
                        result.update({
                            "CapacityGB":capacity_gb,
                            "CapacityTB":round( capacity_gb/1000, 2 ),
                            "PricePerGB":round( result["PriceAUD"]/capacity_gb, 2 ),
                            "PricePerTB":round( result["PriceAUD"]/(capacity_gb/1000), 2 ),
                        })
                        break
            if ("CapacityGB" not in result.keys()):
                print(f"CapacityGB not found in title: {title_split}")
            
            # ### Remove unneeded words
            # ### All remaining elements should be required for: ["Brand", "Series", "ModelNumber"]
            # title_split = remove_multiple_strings_from_list(
            #     title_split,
            #     ["PCIe", "PCI-E", "SSD", "Series", "M.2", "SATA", "2.5in", "NVMe", "NVME", "Gen4"],
            # )

            # ### ["Brand", "Series", "ModelNumber"]
            # if title_split[0] == "Samsung":
            #     # ['Samsung', '870', 'EVO', '2.5in', 'SATA', 'SSD', '500GB']
            #     # ['Samsung', '970', 'EVO', 'Plus', 'NVMe', 'SSD', '1TB']
            #     if title_split[3] == "Plus":
            #         title_split = concaternate_items_within_list(title_split, 2, 3)

            # elif title_split[0] == "ADATA":
            #     if title_split[3] == "Pro":
            #         title_split = concaternate_items_within_list(title_split, 2, 3)
            #     if title_split[4] == "Blade":
            #         title_split = concaternate_items_within_list(title_split, 2, 4)

            # elif title_split[0] == "Western":
            #     # title_split[0] = "Western Digital"
            #     # del title_split[1]
            #     title_split = concaternate_items_within_list(title_split, 0, 1)

            # # elif title_split[0] == ":"
            # #     title_split[0] = "???"
            # #     del title_split[1]

            # # elif title_split[0] == ":"
            # #     title_split[0] = "???"
            # #     del title_split[1]



            ### Preprocess common values
            # capacity = int(title_split[2].strip("TB"))

            ### Update
            # result.update({
            #     "Brand":var,
            #     "Series":var,
            #     "Model":var,
            #     "Capacity":capacity,
            #     "PricePerGB":round(result["PriceAUD"]/capacity, 2),
            # })

            # print(result)
            # print(result)
            # print(json.dumps(result, indent=4))
            # input("\nPress ENTER to continue\n")

            #############################################################################################

            results.append(result)

        return results

