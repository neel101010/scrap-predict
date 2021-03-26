import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(ChromeDriverManager().install())
import requests
from bs4 import BeautifulSoup

url = "https://in.finance.yahoo.com/quote/%5ENSEI/components/"
page = requests.get(url)
print(page)
soup = BeautifulSoup(page.content,'html.parser')
soup = soup.find_all('tr', class_='BdT Bdc($seperatorColor) Ta(end) Fz(s)')
information = []
print(soup[0])
for i in soup:
    lst = []
    temp = i.find_all('td', class_="Py(10px) Ta(start) Pend(10px)")
    name = temp[1].text
    link = temp[0].find_all('a', class_='C($linkColor) Cur(p) Td(n) Fw(500)')
    link = link[0]['href']
    temp = i.find_all('td', class_='Py(10px) Pstart(10px)')
    last_price = temp[0].text
    change = temp[1].text
    per_change = temp[2].text
    volume = temp[3].text
    lst.append(name)
    lst.append(last_price)
    lst.append(change)
    lst.append(per_change)
    lst.append(volume)
    lst.append(link)
    information.append(lst)

print(information)
