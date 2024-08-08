import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup 
import pandas as pd



base = pd.reade_csv(r'database_rooms\database_rooms\parser_avito.py')

driver = webdriver.Chrome()
driver.get("https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYysVLKTczMU7KuBQQAAP__w5qblCAAAAA=2")
wait = WebDriverWait(driver, 10)
time.sleep(1)
driver.refresh()
page = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'index-content-_KxNP')))
htmlString = page.get_attribute("outerHTML")

soup = BeautifulSoup(htmlString, 'html.parser')

elementsBodyBlock = soup.find_all('div', class_='iva-item-body-KLUuy')




for Block in (elementsBodyBlock):
    if len(Block.find_all(attrs={'data-marker': 'item-address'})) > 0:
        elementPrise = Block.find('strong', class_= 'styles-module-root-bLKnd')
        elementInfoRoom = Block.find('h3', class_= 'styles-module-root-GKtmM styles-module-root-YczkZ styles-module-size_l-iNNq9 styles-module-size_l_compensated-KFJud styles-module-size_l-YMQUP styles-module-ellipsis-a2Uq1 styles-module-weight_bold-jDthB stylesMarningNormal-module-root-S7NIr stylesMarningNormal-module-header-l-iFKq3')
        elementAdress = Block.find('p', class_= 'styles-module-root-YczkZ styles-module-size_s-xb_uK styles-module-size_s-_z7mI stylesMarningNormal-module-root-S7NIr stylesMarningNormal-module-paragraph-s-Yhr2e')
        elementMoreInfo = Block.find('p', class_= 'styles-module-root-YczkZ styles-module-size_s-xb_uK styles-module-size_s_compensated-QmHFs styles-module-size_s-_z7mI styles-module-ellipsis-a2Uq1 stylesMarningNormal-module-root-S7NIr stylesMarningNormal-module-paragraph-s-Yhr2e styles-module-noAccent-LowZ8 styles-module-root_bottom-G4JNz styles-module-margin-bottom_6-_aVZm')
        print(elementPrise.text.strip(), elementInfoRoom.text.strip(), elementAdress.text.strip(), '\n', elementMoreInfo.text.strip(), '\n')
    else:
        pass










