import numpy as np
from bs4 import BeautifulSoup
import requests
import urllib3
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from sklearn import model_selection
from sklearn.linear_model import LinearRegression


# Information of all companies
def companyGet():
    url = "https://in.finance.yahoo.com/quote/%5ENSEI/components/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup = soup.find_all('tr', class_='BdT Bdc($seperatorColor) Ta(end) Fz(s)')
    information = {}
    name_lst = []
    last_price_lst = []
    change_lst = []
    per_change_lst = []
    volume_lst = []
    link_lst = []
    for i in soup:
        temp = i.find_all('td', class_="Py(10px) Ta(start) Pend(10px)")
        name = temp[1].text
        link = temp[0].find_all('a', class_='C($linkColor) Cur(p) Td(n) Fw(500)')
        link = link[0]['href']
        temp = i.find_all('td', class_='Py(10px) Pstart(10px)')
        last_price = temp[0].text
        change = temp[1].text
        per_change = temp[2].text
        volume = temp[3].text
        name_lst.append(name)
        last_price_lst.append(last_price)
        change_lst.append(change)
        per_change_lst.append(per_change)
        volume_lst.append(volume)
        link1, link2 = link.split('=')
        link_lst.append(link2)
    information['name'] = name_lst
    information['last_price'] = last_price_lst
    information['change'] = change_lst
    information['per_change'] = per_change_lst
    information['volume'] = volume_lst
    information['link'] = link_lst
    return information


# Company Info
def infoGet(company):
    information = {}
    url = "https://in.finance.yahoo.com/quote/"+company+"/profile?p="+company
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup = soup.find_all('p', class_="Mt(15px) Lh(1.6)")
    description = soup[0].text
    soup = BeautifulSoup(page.content, 'html.parser')
    soup = soup.find_all('h1', class_="D(ib) Fz(18px)")
    name = soup[0].text
    information["description"] = description
    information["company"] = company
    information["name"] = name
    information["closing"] = "NA"
    return information


# Calculation
def closingGet(x, y, company):
    information = {}
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_window_position(-10000, 0)
    driver.get('https://in.finance.yahoo.com/quote/'+company+'/history/')
    try:
        WebDriverWait(driver, 0).until(EC.presence_of_element_located((By.CLASS_NAME, 'Fl(end) Mt(3px) Cur(p)')))
    except TimeoutException:
        print('Page timed out after 0 secs.')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    a = (soup.find('a', {'class': 'Fl(end) Mt(3px) Cur(p)'})['href'])
    df = pd.read_csv(a)
    df = df[["Close"]]
    df.dropna(inplace=True)
    forecast_out = 2
    df["Predict"] = df["Close"].shift(-forecast_out)
    X = np.array(df.drop(["Predict"], 1))
    X = X[:-forecast_out]
    y = np.array(df["Predict"])
    y = y[:-forecast_out]
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    X_forecast = np.array(df.drop(["Predict"], 1))[-forecast_out:]
    # prediction = regressor.predict(X_forecast)
    c = regressor.intercept_
    m = regressor.coef_
    x = float(x)
    close = m * x + c
    close = close.tolist()
    close = close[0]
    information = infoGet(company)
    information['closing'] = close
    return information
