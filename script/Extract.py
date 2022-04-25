#!/usr/bin/python3

### Imports
import datetime

from Web import Web


class Extract: # TODO: Modify class to accept "WEBSITE" programmatically

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
    def combineArrayItems(array, start_i, end_i):
        ### Receives an array, and two indexes
        ### Returns the array, with the elements between the indexes (inclusive) combined into one element
        for _ in range(end_i - start_i):
            array[start_i] = f"{array[start_i]} {array[start_i + 1]}"
            del array[start_i + 1]

        return array

    
    @staticmethod
    def removeStrings(a, strings_a):
        # for s_i, s in enumerate(array):
        #     if s in strings_array:
        #         del array[s_i]
        for s in a:
            if s in strings_a:
                a.remove(s)

        return a

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

            title_a = result["Title"].split()

            ### WEBSITE & CATEGORY SPECIFIC DATA
            ### HDDs
            if category == "hdd":
                ### Remove unneeded words
                title_a = Extract.removeStrings(title_a, ["WD"])
                
                ### Make array consistent to Brand/Series/Model
                if title_a[0] == "Western": # ["Western", "Digital", "WD"] --> ["Western Digital"]
                    title_a = Extract.combineArrayItems(title_a, 0, 1)

                    if title_a[1] == "Red": # ["Red", "Plus"] --> ["Red Plus"]
                        title_a = Extract.combineArrayItems(title_a, 1, 2)

                ### Preprocess common values
                capacity_value = int(title_a[2].strip("TB"))

                ### Update
                result.update({
                    "Brand":title_a[0],
                    "Series":title_a[1],
                    "Model":title_a[3],
                    "CapacityRaw":title_a[2],
                    "CapacityValue":capacity_value,
                    "PricePerTB":round(result["PriceAUD"]/capacity_value, 2),
                })


            ### SSDs
            elif category == "ssd":

                ### "FormFactor"
                if "2.5in" in title_a:
                    result.update({ "FormFactor":"2.5in" })
                elif ("M.2" in title_a) or ("NVMe" in title_a):
                    result.update({ "FormFactor":"M.2" })
                else:
                    print(f"Unable to find a formfactor in title: {title_a}")

                ### "Protocol"
                if "SATA" in title_a:
                    result.update({ "Protocol":"SATA" })
                elif "Gen4" in title_a:
                    result.update({ "Protocol":"NVMe Gen4" })
                elif ("NVMe" in title_a) or ("NVME" in title_a):
                    result.update({ "Protocol":"NVMe Gen3" })
                else:
                    print(f"Unable to find a protocol in title: {title_a}")

                ### "Capacity"
                for s in reversed(title_a):
                    if ("TB" in s):
                        # s = title_a.pop(s) # Remove from list # ERROR, due to "reversed()" converting to a string
                        capacity_value = int(s.strip("TB"))
                        result.update({
                            "CapacityRaw":s,
                            "CapacityValue":capacity_value,
                            "PricePerTB":round(result["PriceAUD"]/capacity_value, 2),
                        })
                        break
                    elif ("GB" in s):
                        # s = title_a.pop(s) # Remove from list
                        capacity_value = int(s.strip("GB"))
                        result.update({
                            "CapacityRaw":s,
                            "CapacityValue":capacity_value,
                            "PricePerTB":round(result["PriceAUD"]/1024*capacity_value, 2),
                        })
                        break
                if "CapacityRaw" not in result.keys():
                    print(f"Unable to find a capacity in title: {title_a}")

                
                ### Remove unneeded words
                ### All remaining elements should be required for: ["Brand", "Series", "ModelNumber"]
                title_a = Extract.removeStrings(
                    title_a, ["PCIe", "PCI-E", "SSD", "Series",
                        "M.2", "SATA", "2.5in", "NVMe", "NVME", "Gen4"]
                )

                ### ["Brand", "Series", "ModelNumber"]
                if title_a[0] == "Samsung":
                    # ['Samsung', '870', 'EVO', '2.5in', 'SATA', 'SSD', '500GB']
                    # ['Samsung', '970', 'EVO', 'Plus', 'NVMe', 'SSD', '1TB']
                    if title_a[3] == "Plus":
                        title_a = Extract.combineArrayItems(title_a, 2, 3)

                elif title_a[0] == "ADATA":
                    if title_a[3] == "Pro":
                        title_a = Extract.combineArrayItems(title_a, 2, 3)
                    if title_a[4] == "Blade":
                        title_a = Extract.combineArrayItems(title_a, 2, 4)

                elif title_a[0] == "Western":
                    # title_a[0] = "Western Digital"
                    # del title_a[1]
                    title_a = Extract.combineArrayItems(title_a, 0, 1)

                # elif title_a[0] == ":"
                #     title_a[0] = "???"
                #     del title_a[1]

                # elif title_a[0] == ":"
                #     title_a[0] = "???"
                #     del title_a[1]

                ### Check for missing "ModelNumber"
                if title_a[2] in ["M.2", "2.5in"]:
                    title_a.insert(2, "")


                # print(["Brand", "Series", "ModelNumber", "FormFactor", "Protocol", "Capacity"])
                print(title_a)

                ### Preprocess common values
                # capacity = int(title_a[2].strip("TB"))

                ### Update
                # result.update({
                #     "Brand":var,
                #     "Series":var,
                #     "Model":var,
                #     "Capacity":capacity,
                #     "PricePerTB":round(result["PriceAUD"]/capacity, 2),
                # })



            elif category == "cpu":
                pass
            elif category == "gpu":
                pass
            else:
                print(f"Unknown category '{category}', exiting...")
                exit(1)


        #     results.append(result)

        # return results

    @staticmethod
    def scorptec():
        pass
