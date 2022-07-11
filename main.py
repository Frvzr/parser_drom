from config import URL
import requests
from bs4 import BeautifulSoup as bs

page = requests.get(URL)
print(page.status_code)

soup = bs(page.text, 'html.parser')

cars = soup.find('div', class_ = 'css-1nvf6xk eaczv700')
#print(cars)

for item in cars:
    a = item.find_all('a', class_ = 'css-5l099z ewrty961')
    car_name = item.find_all('span', {'data-ftid': 'bull_title'})
    

if __name__ == '__main__':
    pass