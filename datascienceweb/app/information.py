from bs4 import BeautifulSoup
import requests


csv_url = "https://in.finance.yahoo.com/quote/RELIANCE.NS/profile?p=RELIANCE.NS"
csv_url = requests.get(csv_url)
soup = BeautifulSoup(csv_url.content, 'html.parser')
a = soup.find('section', {'class': 'quote-sub-section Mt(30px)'})
print(a)