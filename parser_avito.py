import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup 


driver = webdriver.Chrome()
driver.get("https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYysVLKTczMU7KuBQQAAP__w5qblCAAAAA=2")
wait = WebDriverWait(driver, 10)
time.sleep(1)
driver.refresh()
page = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'index-content-_KxNP')))
html_string = page.get_attribute("outerHTML")

soup = BeautifulSoup(html_string, 'html.parser')

elements = soup.find_all('strong', class_='styles-module-root-bLKnd')
for element in elements:
    print(element.text.strip())
    print("🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢")


print(elements)







