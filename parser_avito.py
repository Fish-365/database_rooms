import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup 
import pandas as pd
import re



            # заготовленные функции:
# приведение цены к int строки
def price(priceStr):
    # Очистка строки от лишних пробелов и нормализация
    priceStr = re.sub(r'\s+', ' ', priceStr.strip())
    price = ''

    for char in priceStr:
        if char != ' ':
            price += char
        else:
            pass
    price = price[:-1]
    return int(price)

# этаж и сколько всего этажей
def infoFloor(InfoRoom):
    return InfoRoom[2][:-4].split('/')

# проверка на являестся ли это квартира или студия
def flat(InfoRoom):
    flat = 1 # квартира = 1
    if InfoRoom[0].find('студия') != -1:
        flat = 0 # студия = 0
    return flat 

# расчёт метража
def square(InfoRoom):
    arrSquare = list(InfoRoom[1][:-3])
    if InfoRoom[1][:-3].find(',') != -1:
        indexSquare = arrSquare.index(',')
        arrSquare[indexSquare] = '.'
    else:
        pass
    square = float(''.join(arrSquare))
    return square


def infoRoom_(InfoRoom, priceStr, address):
    InfoRoom = InfoRoom.split(' ')
    for i in range(len(InfoRoom)):
        InfoRoom[i] = re.sub(r'\xa0', ' ', InfoRoom[i])

    if len(InfoRoom) == 4:
        rooms = InfoRoom[0][:-3]
        InfoRoom.pop(0)
        return price(priceStr), rooms, square(InfoRoom), infoFloor(InfoRoom)[0], infoFloor(InfoRoom)[1], flat(InfoRoom) ,address, 
    else:
        rooms = 1
        return price(priceStr), rooms, square(InfoRoom), infoFloor(InfoRoom)[0], infoFloor(InfoRoom)[1], flat(InfoRoom) ,address, 



# подключение selenium  к сайту
driver = webdriver.Chrome()
driver.get("https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYysVLKTczMU7KuBQQAAP__w5qblCAAAAA=2")
wait = WebDriverWait(driver, 10)

time.sleep(1)

# получение html кода страницы
driver.refresh()
page = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'index-content-_KxNP')))
htmlString = page.get_attribute("outerHTML")

# парсинг блоков с объявлениями 
soup = BeautifulSoup(htmlString, 'html.parser')
elementsBodyBlock = soup.find_all('div', class_='iva-item-body-KLUuy')




for Block in (elementsBodyBlock):
    if len(Block.find_all(attrs={'data-marker': 'item-address'})) > 0:
        elementPrice = Block.find('strong', class_= 'styles-module-root-bLKnd')
        elementInfoRoom = Block.find('h3', class_= 'styles-module-root-GKtmM styles-module-root-YczkZ styles-module-size_l-iNNq9 styles-module-size_l_compensated-KFJud styles-module-size_l-YMQUP styles-module-ellipsis-a2Uq1 styles-module-weight_bold-jDthB stylesMarningNormal-module-root-S7NIr stylesMarningNormal-module-header-l-iFKq3')
        elementAdress = Block.find('p', class_= 'styles-module-root-YczkZ styles-module-size_s-xb_uK styles-module-size_s-_z7mI stylesMarningNormal-module-root-S7NIr stylesMarningNormal-module-paragraph-s-Yhr2e')
        elementMoreInfo = Block.find('p', class_= 'styles-module-root-YczkZ styles-module-size_s-xb_uK styles-module-size_s_compensated-QmHFs styles-module-size_s-_z7mI styles-module-ellipsis-a2Uq1 stylesMarningNormal-module-root-S7NIr stylesMarningNormal-module-paragraph-s-Yhr2e styles-module-noAccent-LowZ8 styles-module-root_bottom-G4JNz styles-module-margin-bottom_6-_aVZm')
        print('_________________________', '\n'*2,
            (elementPrice.text.strip()), '\n',
            (elementInfoRoom.text.strip()), '\n',
            elementAdress.text.strip(), '\n', 
            elementMoreInfo.text.strip(), '\n')

        print(infoRoom_(elementInfoRoom.text.strip(), str(elementPrice.text.strip()), elementAdress.text.strip()))
    else:
        pass










