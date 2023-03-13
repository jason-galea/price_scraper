#!/usr/bin/python3

import os
import datetime
import enum
import json

from bs4 import BeautifulSoup as bs
# from selenium import webdriver
from selenium.webdriver import Firefox, DesiredCapabilities
from selenium.webdriver.firefox.options import Options


### FUNCTIONS
def concaternate_items_within_list(l, i, j):
    ### Receives list & two indexes
    ### Returns list with elements between the indexes concaternated (inclusive)
    ### E.G: concaternate_items_within_list(["a", "b", "c", "d"], 1, 2) --> ["a", "b c", "d"]
    for _ in range(j - i):
        l[i] = f"{l[i]} {l[i + 1]}"
        del l[i + 1]

    return l

def remove_multiple_strings_from_list(l=list, strings_to_remove=list):
    return [s for s in l if (s not in strings_to_remove)]

def export_json(extracted_data, dir, file):
    print(f"\nExporting data to {file}\n")

    ### Check/Create dir
    if not os.path.exists(dir):
        os.makedirs(dir)

    ### Write
    with open(file, "w") as f:
        f.write(json.dumps(extracted_data))

# def entrypoint(website, category, export_dir, export_file, debug=False):
def entrypoint(website, category, output_dir, debug=False):
    NOW = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S') 
    # OUT_JSON_DIR = f"{os.path.abspath(os.path.dirname(__file__))}/../out" ### This shit sucks
    OUT_JSON_FILE = f"{output_dir}/{NOW}_{website}_{category}.json"

    match website:
        case "pccg":
            my_extract_instance = PCCG(category)
        case "scorptec":
            my_extract_instance = Scorptec(category)
        case "centrecom":
            my_extract_instance = Centrecom(category)

    ### Download HTML
    bs4_html = my_extract_instance.download_html()

    ### Extract
    extracted_data = my_extract_instance.extract(bs4_html)

    ### Debug
    if (debug):
        print(json.dumps(extracted_data, indent=4))

    ### Export
    export_json(extracted_data, output_dir, OUT_JSON_FILE)

    ### Cleanup
    os.system('pkill firefox') ### Lol. Lmao
    return


### CLASSES
class PCCG:
    URLS = {
        "hdd": "https://www.pccasegear.com/category/210_344/hard-drives-ssds/3-5-hard-drives",
        "ssd": "https://www.pccasegear.com/category/210_902/hard-drives-ssds/solid-state-drives-ssd",
        "cpu": "",
        "gpu": "",
    }

    def __init__(self, category) -> None:
        self.category = category

    def download_html(self, url=""):

        ### Workaround for not being able to use "self.var" as default value
        if (url == ""):
            url = self.URLS[self.category]

        ### Options
        ff_opts = Options()
        ff_opts.add_argument('-headless')
        ff_cap = DesiredCapabilities.FIREFOX
        ff_cap["marionette"] = True

        # driver = webdriver.Firefox(
        driver = Firefox(
            options=ff_opts,
            capabilities=ff_cap,
        )

        ### Request page
        driver.get(url)

        ### Return BS object, containing parsed HTML
        ### TODO: Explicitely fulfil parameters
        return bs(
            driver.page_source,
            "html.parser"
        )

    def extract(self, bs4_html):
        match self.category:
            case "hdd":
                return self._extract_hdd_data(bs4_html)
            case "ssd":
                return self._extract_hdd_data(bs4_html)

    def _extract_hdd_data(bs4_html):
        pass

    def _extract_sdd_data():
        pass

class Scorptec:
    URLS = {
        "hdd": "",
        "ssd": "",
        "cpu": "",
        "gpu": "",
    },

    def __init__(self, category) -> None:
        self.category = category
        
    def download_html(): pass

    def _extract_hdd_data(): pass

    def _extract_sdd_data(): pass

class Centrecom:
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


def pccg(category, soup):
    
    results = []

    for product in soup.find_all("div", class_="product-container"):

        ### Setup & data common to PCCG
        result = {
            "UTCTime":  datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S"),
            "Retailer": "PCCG",
            "Title":    product.find_next("a", class_="product-title").string,
            "URL":      product.find_next("a", class_="product-title").attrs["href"],
            "PriceAUD": int(product.find_next("div", class_="price").string.strip("$")),
        }

        ### TODO: Fetch full description from current products "url"
        # description_soup = Web.get_BS4_HTML_from_URL(result["URL"])
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


        ### WEBSITE & CATEGORY SPECIFIC DATA
        if category == "hdd":
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


        elif category == "ssd":

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


        elif category == "cpu":
            pass
        elif category == "gpu":
            pass
        else:
            print(f"Unknown category '{category}', exiting...")
            exit(1)


        results.append(result)

    return results