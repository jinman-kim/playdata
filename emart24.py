from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
import requests

emart_url = "https://www.emart24.co.kr/store"
driver = webdriver.Chrome()
driver.get(emart_url)
driver.find_element(By.CLASS_NAME,'valueList.sidoList.open').click()
bs = BS(driver.page_source)
a = bs.find('li')['value']
print(a)
