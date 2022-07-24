#!/usr/bin/python3

import datetime
import enum
import json

from Web import Web


class Extract:

    @staticmethod
    def extract(website, category, soup):
        if website == "pccg":
            return Extract.pccg(category, soup)
        elif website == "scorptec":
            pass
        elif website == "centrecom":
            pass
        # elif website == "???":
        #     pass


    @staticmethod
    def combineArrayItems(a, i, j):
        ### Receives array & two indexes
        ### Returns array with elements between the indexes (inclusive) concaternated
        for _ in range(j - i):
            a[i] = f"{a[i]} {a[i + 1]}"
            del a[i + 1]

        return a

    
    @staticmethod
    def removeStrings(a, strings_a):
        return [s for s in a if (s not in strings_a)]

    @staticmethod
    def pccg(category, soup):
        
        results = []

        for product in soup.find_all('div', class_="product-container"):

            ### Setup & data common to PCCG
            result = {
                "UTCTime": datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S"),
                "Retailer": "PCCG",
                "Title":product.find_next("a", class_="product-title").string,
                "URL":product.find_next("a", class_="product-title").attrs["href"],
                "PriceAUD":int(product.find_next("div", class_="price").string.strip("$")),
            }

            ### TODO: Fetch full description from current products "url"
            # description_soup = Web.GetPageSoup(result["URL"])
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
            print(title_split)


            ### Discard unwanted items
            if ("Upgrade" in title_split): continue


            ### WEBSITE & CATEGORY SPECIFIC DATA
            if category == "hdd":
                ### Remove unneeded words
                title_split = Extract.removeStrings(title_split, ["WD"])
                
                ### Make array consistent to Brand/Series/Model
                if title_split[0] == "Western": # ["Western", "Digital", "WD"] --> ["Western Digital"]
                    title_split = Extract.combineArrayItems(title_split, 0, 1)

                    if (title_split[1] == "Red") and (title_split[2] in ["Plus", "Pro"]):
                        title_split = Extract.combineArrayItems(title_split, 1, 2)

                print(title_split)

                ### Preprocess common values
                capacity_gb = int(title_split[2].strip("TB"))*1024
                capacity_tb = round(capacity_gb/1024, 2)

                ### Save
                result.update({
                    "Brand":title_split[0],
                    "Series":title_split[1],
                    "Model":title_split[3],
                    # "CapacityRaw":title_split[2],
                    "CapacityGB":capacity_gb,
                    "PricePerGB":round(result["PriceAUD"]/capacity_gb, 2),
                    "CapacityTB":capacity_tb,
                    "PricePerTB":round(result["PriceAUD"]/capacity_tb, 2),
                })


            elif category == "ssd":

                ### Common 1:1 matches
                ### "FormFactor", "Protocol", "Brand"
                ### TODO: Use REGEX instead?
                common_dicts = {
                    "FormFactor":{
                        "2.5in":"2.5in",
                        "M.2":"M.2",
                        "NVMe":"M.2",
                        "NVME":"M.2",
                    },
                    "Protocol":{
                        "SATA":"SATA",
                        "Gen4":"NVMe Gen4",
                        "NVMe":"NVMe Gen3",
                        "NVME":"NVMe Gen3",
                    },
                    "Brand":{
                        "Samsung":"Samsung",
                        "ADATA":"ADATA",
                        "Corsair":"Corsair",
                        "Kingston":"Kingston",
                        "MSI":"MSI",
                        "Team":"Team",
                        "Western":"Western Digital",
                        "Gigabyte":"Gigabyte",
                    }
                }            
                for col, dict in common_dicts.items():
                    for key, val in dict.items():
                        if (key in title_split):
                            result.update({ col:val })
                            break
                    if (col not in result.keys()):
                        print(f"{col} not found in title: {title_split}")

                ### "CapacityGB", "PricePerGB", "PricePerGB"
                capacity_dict = {
                    "TB":1024,
                    "GB":1,
                }
                for label, val in capacity_dict.items():
                    for s in reversed(title_split):
                        if (label in s):
                            capacity_gb = int(s.strip(label))*val
                            result.update({
                                "CapacityGB":capacity_gb,
                                # "CapacityTB":capacity_gb/1024,
                                "CapacityTB":round( capacity_gb/1024, 2 ),
                                "PricePerGB":round( result["PriceAUD"]/capacity_gb, 2 ),
                                "PricePerTB":round( result["PriceAUD"]/(capacity_gb/1024), 2 ),
                            })
                            break
                if ("CapacityGB" not in result.keys()):
                    print(f"CapacityGB not found in title: {title_split}")
                
                # ### Remove unneeded words
                # ### All remaining elements should be required for: ["Brand", "Series", "ModelNumber"]
                # title_split = Extract.removeStrings(
                #     title_split, ["PCIe", "PCI-E", "SSD", "Series",
                #         "M.2", "SATA", "2.5in", "NVMe", "NVME", "Gen4"]
                # )

                # ### ["Brand", "Series", "ModelNumber"]
                # if title_split[0] == "Samsung":
                #     # ['Samsung', '870', 'EVO', '2.5in', 'SATA', 'SSD', '500GB']
                #     # ['Samsung', '970', 'EVO', 'Plus', 'NVMe', 'SSD', '1TB']
                #     if title_split[3] == "Plus":
                #         title_split = Extract.combineArrayItems(title_split, 2, 3)

                # elif title_split[0] == "ADATA":
                #     if title_split[3] == "Pro":
                #         title_split = Extract.combineArrayItems(title_split, 2, 3)
                #     if title_split[4] == "Blade":
                #         title_split = Extract.combineArrayItems(title_split, 2, 4)

                # elif title_split[0] == "Western":
                #     # title_split[0] = "Western Digital"
                #     # del title_split[1]
                #     title_split = Extract.combineArrayItems(title_split, 0, 1)

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
                print(json.dumps(result, indent=4))
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

    @staticmethod
    def scorptec():
        pass
