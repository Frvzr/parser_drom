from config import URL
import requests
from bs4 import BeautifulSoup as bs

page = requests.get(URL)
print(page.status_code)

soup = bs(page.text, 'html.parser')

cars = soup.find_all('div', class_ = 'css-1nvf6xk eaczv700')
for car in cars:
    link = 
    name = 
    description =
    

if __name__ == '__main__':
    pass