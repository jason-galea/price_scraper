#!/usr/bin/python3

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

# header = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
url = "https://www.pccasegear.com/category/210_344/hard-drives-ssds/3-5-hard-drives"
result = []


### PREP
# Start driver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
# driver.implicitly_wait(3)

driver.get(url)

# Sort price low to high
# driver.find_element_by_css_selector("div[role='combobox']").click()
# driver.find_element_by_id("downshift-1-item-1").click() # "No element found"

# Hand content to BS
soup = bs(driver.page_source, "html.parser")


### EXTRACT DATA
for a in soup.find_all('div', class_="product-container"):
    print(a)



