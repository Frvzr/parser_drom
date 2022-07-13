# -*- coding: utf-8 -*-

from config import URL
import requests
from bs4 import BeautifulSoup as bs
import re
import openpyxl

def get_request(url):
    page = requests.get(url)
    print(page.status_code) 
    return soup_data(page)

def soup_data(page):
    soup = bs(page.text, 'html.parser')
    cars = soup.find_all('a', class_ = 'css-5l099z ewrty961')
    return collect_data(cars)

def collect_data(cars):
    cars_dict = {}
    for car in cars:
        link = car.get('href')
        id = re.findall('\d{8}', str(link))
        car_name = car.find('span', {'data-ftid': 'bull_title'}).text.split(',')
        desc = car.find('span', {'data-ftid': 'bull_description-item'}).contents
        price = car.find('span', {'data-ftid': 'bull_price'}).text
        price_ = re.sub(r"\s+", "", price)
        desc = car.find_all('span', class_ = 'css-1l9tp44 e162wx9x0')
        description = []
        for i in desc:
            description.append(i.text.strip(','))

        cars_dict.setdefault(*id, [*car_name, *description, link, price_])

    #print(cars_dict)
    return create_file(cars_dict)

def create_file(cars_dict):
    try:
        wb = openpyxl.load_workbook('cars.xlsx')
        ws = wb.active
    except:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['id', 'car_name', 'year', 'engine', 'fuel', 'transmissions', 'drive', 'mileage', 'link', 'price'])
    for row, (key, values) in enumerate(cars_dict.items(), start=2):
        ws[f'A{row}'] = key
        ws[f'B{row}'] = values[0]
    return save_excel(wb)

def save_excel(wb):
    try:
        f_name = f'cars.xlsx'       
        wb.save(f_name)
        message = f'данные записаны в файл \n'
    except:
        message = f'ошибка записи в файл \n'
    finally:
        wb.close
        print(message)

if __name__ == '__main__':
    get_request(URL)