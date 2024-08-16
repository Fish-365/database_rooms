import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup 
import pandas as pd
import re
import languagemodels as lm

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'




            # заготовленные функции:
# приведение цены к int строки
def price(priceStr):
    # Очистка строки от лишних пробелов и нормализация
    priceStr = re.sub(r'\s+', '', priceStr.strip())
    priceStr = re.sub(r'\D', '', priceStr)
    price = priceStr[:-1]
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

def address_(address_arr):
    if len(address_arr) == 3:
        address = address_arr[1].text.strip()
    elif len(address_arr) == 2:
        address = address_arr[0].text.strip()
    else:
        address = address_arr[0].text.strip()

    return address



def infoRoom_(InfoRoom, priceStr, address):
    InfoRoom = InfoRoom.split(' ')
    for i in range(len(InfoRoom)):
        InfoRoom[i] = re.sub(r'\xa0', ' ', InfoRoom[i])

    if len(InfoRoom) > 4:
        for i in range( len(InfoRoom)- 4):
            InfoRoom.pop(0)

    if len(InfoRoom) == 4:
        rooms = InfoRoom[0][:-3]
        InfoRoom.pop(0)
        return price(priceStr), rooms, square(InfoRoom), infoFloor(InfoRoom)[0], infoFloor(InfoRoom)[1], flat(InfoRoom) ,address_(address)
    else:
        rooms = 1
        return price(priceStr), rooms, square(InfoRoom), infoFloor(InfoRoom)[0], infoFloor(InfoRoom)[1], flat(InfoRoom) ,address_(address)



shapka = {'prise': [], 'rooms': [], 'square': [], 'floor': [], 'totalFloors': [], 'flat/studio': [], 'address': [], 'coordinate': [], "distanceFromTheCenter": [], 'metro': [], 'cafe': [], 'park': [], 'beaches': [], 'hospital': [], 'police': [], 'shop': [], 'beautySalone': [], 'mall': [], 'museum': [], 'pharmacy': [], 'sportCenter': [], 'postOffice': [], 'hotel': []}
df = pd.DataFrame(shapka)

# подключение selenium  к сайту
driver = webdriver.Edge()
driver.get("https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYysVLKTczMU7KuBQQAAP__w5qblCAAAAA&p=100")
wait = WebDriverWait(driver, 10)
driver.refresh()

for i in range(100):
    time.sleep(1)

    # получение html кода страницы
    
    page = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'index-content-_KxNP')))
    htmlString = page.get_attribute("outerHTML")

    # парсинг блоков с объявлениями 
    soup = BeautifulSoup(htmlString, 'html.parser')
    elementsBodyBlock = soup.find_all('div', class_='iva-item-body-KLUuy')




    for Block in (elementsBodyBlock):
        if len(Block.find_all(attrs={'data-marker': 'item-address'})) > 0:
            elementPrice = Block.find('strong', class_= 'styles-module-root-bLKnd')
            elementInfoRoom = Block.find('h3', class_= 'styles-module-root-GKtmM styles-module-root-YczkZ styles-module-size_l-iNNq9 styles-module-size_l_compensated-KFJud styles-module-size_l-YMQUP styles-module-ellipsis-a2Uq1 styles-module-weight_bold-jDthB stylesMarningNormal-module-root-S7NIr stylesMarningNormal-module-header-l-iFKq3')
            elementAdress = Block.find_all('p', class_= 'styles-module-root-YczkZ styles-module-size_s-xb_uK styles-module-size_s-_z7mI stylesMarningNormal-module-root-S7NIr stylesMarningNormal-module-paragraph-s-Yhr2e')
            elementMoreInfo = Block.find('p', class_= 'styles-module-root-YczkZ styles-module-size_s-xb_uK styles-module-size_s_compensated-QmHFs styles-module-size_s-_z7mI styles-module-ellipsis-a2Uq1 stylesMarningNormal-module-root-S7NIr stylesMarningNormal-module-paragraph-s-Yhr2e styles-module-noAccent-LowZ8 styles-module-root_bottom-G4JNz styles-module-margin-bottom_6-_aVZm')
            if elementPrice != None and elementInfoRoom != None and elementAdress != [] and elementAdress != None:
                # print('_________________________', '\n'*2,
                #     (elementPrice.text.strip()), '\n',
                #     (elementInfoRoom.text.strip()), '\n',
                #     elementAdress.text.strip(), '\n', 
                #     elementMoreInfo.text.strip(), '\n')

                parseRooms = (infoRoom_(elementInfoRoom.text.strip(), str(elementPrice.text.strip()), elementAdress))
                print(parseRooms)

                data = {
                    'prise': parseRooms[0],
                    'rooms': parseRooms[1],
                    'square': parseRooms[2],
                    'floor': parseRooms[3],
                    'totalFloors': parseRooms[4],
                    'flat/studio': parseRooms[5],
                    'address': parseRooms[6]
                }

                df = pd.concat([df, pd.DataFrame.from_records([data])] ,ignore_index=True)
            else:
                print('🔴 NONE element')
        else:
            pass
    
    df.to_csv('database_rooms\database_rooms\database2.csv', index=False)

    print('➡ page Number:' + str(i+2))
    driver.get(f"https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYysVLKTczMU7KuBQQAAP__w5qblCAAAAA&p={i+102}")



print(df.to_string())
df.to_csv('database_rooms\database_rooms\database2.csv', index=False)







