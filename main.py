# -*- coding: utf-8 -*-

from config import URL
import requests
from bs4 import BeautifulSoup as bs
import re
import openpyxl
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.styles import Alignment

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
    return create_file(cars_dict)

def get_qty_cars():
    pass

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
    return format_file(wb, ws)

def format_file(wb, ws):
    #qty_cars = get_qty_cars()
    #tab = Table(displayName="Table1", ref="A1:J{}".format(qty_cars))
    tab = Table(displayName="Table1", ref="A1:J50")
    style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    tab.tableStyleInfo = style
    ws.add_table(tab)
    col_dimensions = {'A': 15, 'B': 20, 'C': 12, 'D': 12, 'E': 15, 'F': 15, 'G': 15, 'H': 15, 'I': 30, 'J': 15}
    for i in range(50):
        ws.row_dimensions[i].height = 20
    for key, value in col_dimensions.items():
        ws.column_dimensions[key].width = value  
    return save_excel(wb)

def save_excel(wb):
    try:
        f_name = f'C:\\Users\\user\\Desktop\\cars.xlsx'       
        wb.save(f_name)
        message = f'данные записаны в файл \n'
    except:
        message = f'ошибка записи в файл \n'
    finally:
        wb.close
        print(message)

if __name__ == '__main__':
    get_request(URL)