# -*- coding: utf-8 -*-

from config import URL
import requests
from bs4 import BeautifulSoup as bs
import re

page = requests.get(URL)
print(page.status_code)

soup = bs(page.text, 'html.parser')

cars_dict = {}
cars = soup.find_all('a', class_ = 'css-5l099z ewrty961')

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
        desc.append(i.text.strip(','))

    cars_dict.setdefault(*id, [*car_name, *description, link, price_])

print(cars_dict)


if __name__ == '__main__':
    pass