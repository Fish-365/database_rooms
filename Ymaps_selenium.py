import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup 
import pandas as pd
from fake_useragent import UserAgent

driver = webdriver.Chrome()
driver.get("https://Yandex.ru/maps")
wait = WebDriverWait(driver, 10)

address = "пр-д Шмитовский, вл. 40"

def convert_coordinate(coordinate):
    if coordinate != None:
        coordinate_arr = (coordinate.text.strip()).split(',')
        width = coordinate_arr[0]
        longitude = coordinate_arr[1]
        convert_coordinate = str(longitude) + ',' + str(width)
    else:
        convert_coordinate = ''
    return convert_coordinate

def get_coordinate(address):
    # Получаем id элемента для обноружения строки поиска
    input_element_id = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'input__context')))
    html_id = input_element_id.get_attribute("outerHTML")
    id_Ymap = html_id[80:116]

    # Пишем свой запрос в полученное раннее поле
    input_element = wait.until(EC.presence_of_element_located((By.ID, id_Ymap)))
    driver.execute_script("arguments[0].value = '';", input_element)
    input_element.clear()
    input_element.send_keys(address + Keys.RETURN)
    time.sleep(2) 
    page = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sidebar-view__panel')))
    htmlString = page.get_attribute("outerHTML")

    soup = BeautifulSoup(htmlString, 'html.parser')
    coordinate = soup.find('div', class_='toponym-card-title-view__coords-badge')

    input_element.clear()
    return convert_coordinate(coordinate)


ua = UserAgent()

df = pd.read_csv('database_rooms\database_rooms\database.csv')
address_arr = df['address']

time.sleep(10)

for i in range(len(address_arr)):
    coordinate = get_coordinate(address_arr[i])
    df.loc[i, 'coordinate '] = coordinate
    print(df['address'][i], coordinate, str(i))
    time.sleep(0.5)

    if (i % 10) == 0:
        new_user_agent = ua.random
        driver.execute_script("navigator.userAgent = arguments[0]", new_user_agent)


df.to_csv('database.csv', index=False)
print(df)
# print('convert:', get_coordinate(address=address))
# print('convert:', get_coordinate(address='Ленинградское ш., стр. 7.3'))
# time.sleep(1000)