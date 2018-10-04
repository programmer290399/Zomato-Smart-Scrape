"""
Python class to scrap data for a particular restaurant whose zomato link is given
"""

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

browser = None
try:
    browser = webdriver.Firefox()
except Exception as error:
    print(error)


class ZomatoRestaurant:
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
            #print(self.html_text)
            self.soup = BeautifulSoup(self.html_text, 'lxml')

    def scrap(self):
        if self.soup is None:
            return {}
        soup = self.soup
        menu_details = dict()

        name_anchor = soup.find('a', attrs={'class': 'o2header-title'})
        if name_anchor:
            menu_details['restaurant_name'] = name_anchor.text.strip()
        else:
            menu_details['restaurant_name'] = ''


        menu_details['dish_mappings'] = []
        for div in soup.find_all("div", attrs={'class': 'col-s-10 col-m-13'}):
            child_div_dish_name = div.find("div", attrs={'class': 'header'})
            child_div_dish_price = div.find("div", attrs={'class': 'description'})

            if child_div_dish_name:
                dish_detail = dict()
                trim = re.compile(r'[^\d.,]+')
                dish_detail['dish_name'] = child_div_dish_name.text.strip() 
                dish_detail['dish_price'] = trim.sub('',child_div_dish_price.text.strip())
                menu_details['dish_mappings'].append(dish_detail)
        return menu_details


if __name__ == '__main__':
    if browser is None:
        sys.exit()
    out_file = open("zomato_menu.json", "a")
    with open("order_online_menu.txt", "r", encoding="utf-8") as f:
        for line in f:
            zr = ZomatoRestaurant(line)
            json.dump(zr.scrap(), out_file)
            out_file.write('\n')
    out_file.close()
    browser.close()
