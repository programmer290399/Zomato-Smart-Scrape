from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
options = Options()
browser = webdriver.Firefox(firefox_options=options,executable_path=r'D:\21-18\desktop\rps\python\Zomato_smart_scrape\geckodriver.exe')
browser.get('https://www.zomato.com/indore/nafees-restaurant-old-palasia/order')
try:
    element = WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.ID, "navbar_0"))
    )
except:
	print('None')
el = browser.find_elements_by_class_name('header')
for i in el:
	print(i.text)