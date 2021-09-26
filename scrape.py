from typing import Dict
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs


### CONSTANTS
# header = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
url = "https://www.pccasegear.com/category/210_344/hard-drives-ssds/3-5-hard-drives"


### PREP
# Start driver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
# driver.implicitly_wait(1)

driver.get(url)

# Sort price low to high
driver.find_element_by_xpath("//div[@class = 'cat-filter']//div[@role = 'combobox']").click()
driver.find_element_by_xpath("//li[text()[contains(., 'Price (low to high)')]]").click()


# Hand content to BS
soup = bs(driver.page_source, "html.parser")


### EXTRACT DATA
product_data = []
for product in soup.find_all('div', class_="product-container"):
    p_title = product.find_next("a", class_="product-title").string
    p_url = product.find_next("a", class_="product-title").attrs["href"]
    p_desc = product.find_next("p").string
    p_price_aud = int(product.find_next("div", class_="price").string.strip("$")) # "$123" --> 123

    p_title_array = p_title.split()
    p_desc_array = p_desc.split()

    p_hdd_capacity = int(next(x for x in p_title_array if x.__contains__("TB")).strip("TB")) # "10TB" --> 10

    p_hdd_price_per_tb = round(p_price_aud/p_hdd_capacity, 2)


    product_data.append({
        "title": p_title
        , "url": p_url
        , "description": p_desc
        , "price": p_price_aud
        , "hdd_capacity": p_hdd_capacity
        , "hdd_price_per_tb": p_hdd_price_per_tb
    })


for product in product_data:
    for key, value in product.items():
        print("{0} : {1}".format(key, value))
    print()

