import re
import urllib
from urllib import parse
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.request
from selenium import webdriver
from bs4 import NavigableString
import sys
import json
import time 
import locale
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def download(url):
    urllib.request.urlretrieve(url, url.split('/')[-1])


browser = None
try:
    browser = webdriver.Firefox()
except Exception as error:
    print(error)


class Image_finder:
    def __init__(self, url):
        self.url = url
        # print("opening")
        self.html_text = None
        try:
            browser.get(self.url)
            time.sleep(5)
            self.html_text = browser.page_source

            # self.html_text = urllib.request.urlopen(url).read().decode('utf-8')
            # self.html_text = requests.get(url).text
        except Exception as err:
            print(str(err))
            return
        else:
            print('Access successful.')

        self.soup = None
        if self.html_text is not None:
            
            self.soup = BeautifulSoup(self.html_text, 'lxml')

    
    
    
    def scrap_image(self):
        if self.soup is None:
            return {}
        soup = self.soup


        list_len = soup.find('div', attrs={'class': 'pagination-meta left'})
        list_len = int(list_len.text.strip().split()[3])
        for i in range(1,list_len):
            

            html_text = browser.page_source
            soup = BeautifulSoup(html_text, 'lxml')
            

            div = soup.find('div', attrs={"id":"menu-image"})
            image = div.find('img') 
            print("Downloading:" ,image['src'])
            download(image['src'])
            time.sleep(5)
            wait = WebDriverWait(browser , 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-next-page"]')))
            element.click()

if __name__ == '__main__':
    img = Image_finder('https://www.zomato.com/indore/o2-cafe-de-la-ville-new-palasia/menu#tabtop')
    img.scrap_image()
