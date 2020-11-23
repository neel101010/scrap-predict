import numpy as np
from bs4 import BeautifulSoup
import requests
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
    information = {}
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_window_position(-10000, 0)
    driver.get('https://in.finance.yahoo.com/quote/%5ENSEI/components?p=%5ENSEI')
    try:
        WebDriverWait(driver, 0).until(EC.presence_of_element_located((By.CLASS_NAME, 'smartphone_Px(20px)')))
    except TimeoutException:
        print('Page timed out after 0 secs.')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    company_details_list = soup.find_all('a', {'class': 'C($linkColor) Cur(p) Td(n) Fw(500)'})
    company_list = []
    for company in company_details_list:
        company_list.append(company['title'])
    information['company_list'] = company_list
    return information


# Company Info
def infoGet(company):
    information = {}
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_window_position(-10000, 0)
    driver.get("https://in.finance.yahoo.com/quote/"+company+"/profile?p="+company)
    try:
        WebDriverWait(driver, 0).until(EC.presence_of_element_located((By.CLASS_NAME, 'quote-sub-section Mt(30px)')))
    except TimeoutException:
        print('Page timed out after 0 secs.')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    description = soup.find('section', {'class': 'quote-sub-section Mt(30px)'})
    description = description.find_all('p')
    information['description'] = description
    information['company'] = company
    return information


# Calculation
def closingGet(x, company):
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
    information['closing'] = str(close)
    return information

