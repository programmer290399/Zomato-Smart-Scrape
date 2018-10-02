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

    def scrap(self):
        if self.soup is None:
            return {}
        soup = self.soup
        menu_details = dict()

        name_anchor = soup.find("a", attrs={"class": "o2header-title"})
        if name_anchor:
            menu_details['restaurant_name'] = name_anchor.text.strip()
        else:
            menu_details['restaurant_name'] = ''


        # rest_details['what_people_love_here'] = []
        # for div in soup.find_all("div", attrs={'class': 'rv_highlights__section pr10'}):
        #     child_div = div.find("div", attrs={'class': 'grey-text'})
        #     if child_div:
        #         rest_details['what_people_love_here'].append(child_div.get_text())
        # return rest_details


        menu_details['dish_mappings'] = []
        for div in soup.find_all("div", attrs={'class': 'ui item item-view'}):
            child_div_dish_name = div.find("div", attrs={'class': 'header'})
            child_div_dish_price = div.find("div", attrs={'class': 'description'})
            menu_details['dish_detail']=[]
            if child_div_dish_name:
                dish_detail['dish_name'].append(child_div_dish_name.get_text())
                dish_detail['dish_price'].append(child_div_dish_price.get_text())
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
