# -*- coding: utf-8 -*-

from config import URL
import requests
from bs4 import BeautifulSoup as bs
import re
import openpyxl
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.styles import Alignment
import time
import datetime


def get_request(url):
    headers = {"Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    page = requests.get(url, headers=headers)
    print(page.status_code) 
    return soup_data(page)

def soup_data(page):
    soup = bs(page.text, 'html.parser')
    cars = soup.find_all('a', class_ = 'css-5l099z ewrty961')
    return collect_data(cars)

def collect_data(cars):
    cars_dict = {}
    fuel_list = ['бензин', 'дизель', 'электро', 'гибрид', 'гбо']
    transmissions_list = ['автомат', 'акпп', 'робот', 'вариатор', 'механика']
    drive_list = ['4wd', 'передний', 'Задний']
    fuel = ''
    transmission = ''
    drive = ''
    for car in cars:
        description = []
        link = car.get('href')
        id = re.findall('\d{8}', str(link))
        car_name = car.find('span', {'data-ftid': 'bull_title'}).text.split(',')
        price = car.find('span', {'data-ftid': 'bull_price'}).text
        price_ = re.sub(r"\s+", "", price)
        desc = car.find_all('span', class_ = 'css-1l9tp44 e162wx9x0')
        for i in desc:
            description.append(i.text.strip(','))

        try:
            engine = re.findall(r"\d{1}\.\d{1}", str(description))
        except:
            engine = ' '

        try:
            hp = re.findall(r"\d{3} [л]\.[с]", str(description))
        except:
            hp = ' '

        for fuel_type in description:
            if fuel_type.lower() in fuel_list:
                fuel = fuel_type
                break
            else:
                fuel = ' '

        for transmissions_type in description:      
            if transmissions_type.lower() in transmissions_list:
                transmission = transmissions_type
                break
            else:
                transmission = ' '

        for drive_type in description:
            if drive_type.lower() in drive_list:
                drive = drive_type
                break
            else:
                drive = ' '

        try:
            mileage = re.findall(r"[0-9]+ тыс\. км", str(description))
        except:
            mileage = ' '

        cars_dict.setdefault(*id, [*car_name, *engine, *hp, fuel, transmission, drive, *mileage, link, price_])
    return create_file(cars_dict)

def get_qty_cars():
    pass

def create_file(cars_dict):
    try:
        wb = openpyxl.load_workbook(f'C:\\Users\\user\\Desktop\\cars.xlsx')
        ws = wb.active
    except:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['id', 'car_name', 'year', 'engine', 'hp', 'fuel', 'transmissions', 'drive', 'mileage', 'link', 'price ' + datetime.datetime.today().strftime('%Y-%m-%d')])
    maximum_row = ws.max_row   
    for row, (key, values) in enumerate(cars_dict.items(), start=maximum_row+1):
        ws[f'A{row}'] = key
        ws[f'B{row}'] = values[0]
        ws[f'C{row}'] = values[1]
        ws[f'D{row}'] = values[2]
        ws[f'E{row}'] = values[3]
        ws[f'F{row}'] = values[4]
        ws[f'G{row}'] = values[5]
        ws[f'H{row}'] = values[6]
        ws[f'I{row}'] = values[7]
        ws[f'J{row}'] = values[8]
        ws[f'K{row}'] = values[9]
        
    return format_file(wb, ws)

def format_file(wb, ws):
    maxi = ws.max_row
    tab = Table(displayName="Table1", ref=f"A1:K{maxi}")
    style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    tab.tableStyleInfo = style
    try:
        ws.add_table(tab)
    except:
        pass
    col_dimensions = {'A': 15, 'B': 20, 'C': 12, 'D': 12, 'E': 15, 'F': 15, 'G': 15, 'H': 15, 'I': 15, 'J': 50, 'K': 20}
    for i in range(maxi):
        ws.row_dimensions[i].height = 20
    for key, value in col_dimensions.items():
        ws.column_dimensions[key].width = value
    return save_excel(wb)

def save_excel(wb):
    try:
        f_name = f'C:\\Users\\user\\Desktop\\cars.xlsx'       
        wb.save(f_name)
        message = f'данные записаны в файл'
    except:
        message = f'ошибка записи в файл'
    finally:
        wb.close
        print(message)

def main(url):
    start = time.time()
    get_request(url)
    end = time.time()
    print(end - start)


if __name__ == '__main__':
    main(URL)