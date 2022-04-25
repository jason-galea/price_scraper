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
            if category == "hdd":
                
                ### Clean up array, for consistency across brands
                if title_a[0] == "Western": # ["Western", "Digital", "WD"] --> ["Western Digital"]
                    title_a[0] = "Western Digital"
                    del title_a[1:3]

                    if title_a[1] == "Red": # ["Red", "Plus"] --> ["Red Plus"]
                        title_a[1] = f"Red {title_a[2]}" # "Red Plus" or "Red Pro"
                        del title_a[2]

                ### Prepare
                hdd_capacity = int(title_a[2].strip("TB"))

                ### Update
                result.update({
                    "Brand":title_a[0],
                    "Series":title_a[1],
                    "ModelNumber":title_a[3],
                    "HDDCapacity":hdd_capacity,
                    "HDDPricePerTB":round(result["PriceAUD"]/hdd_capacity, 2),
                })


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
