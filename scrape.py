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
# try:
#     dropdown_menu = driver.find_element_by_css_selector("div[aria-labelledby='downshift-1-label']")
# except:
#     dropdown_menu = driver.find_element_by_css_selector("div[aria-labelledby='downshift-4-label']")

# dropdown_menu = driver.find_element("div", value="SORT BY")
# dropdown_menu.click()
# dropdown_price_low_high = driver.find_element_by_id("downshift-4-item-1")
# dropdown_price_low_high.click()

# driver.find_element_by_css_selector("div[aria-labelledby='downshift-4-label']").click()
# driver.implicitly_wait(1)
# driver.find_element_by_id("downshift-4-item-1").click()

# Hand content to BS
soup = bs(driver.page_source, "html.parser")


### EXTRACT DATA
result = []
for a in soup.find_all('div', class_="product-container"):
    title = a.find_next()
    url = a.find_next()
    description = a.find_next()



    pass




