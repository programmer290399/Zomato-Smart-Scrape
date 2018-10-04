
import re
import urllib
from urllib import parse
from bs4 import BeautifulSoup
from pprint import pprint
from urllib.parse import urlparse
import urllib.request
from selenium import webdriver
from bs4 import NavigableString
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from google_images_download import google_images_download 

browser = None

try:
    browser = webdriver.Firefox()
except Exception as error:
    print(error)

out_file = open("Indore_restaurant_links.txt", "wb+")

def download(url):
    urllib.request.urlretrieve(url, url.split('/')[-1])

class Image_finder:
    def __init__(self, url):
        self.url = url
        
        self.html_text = None
        try:
            browser.get(self.url)
            time.sleep(5)
            self.html_text = browser.page_source

           
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

class ZomatoRestaurantLinkGen:
    def __init__(self, url):
        self.url = url
        self.html_text = None
        try:
            browser.get(self.url)
            self.html_text = browser.page_source

        except Exception as err:
            print(str(err))
            return
        else:
            print('Access successful.')

        self.soup = None
        if self.html_text is not None:
            self.soup = BeautifulSoup(self.html_text, 'lxml')

    def scrap_rest_links(self):
        soup = self.soup
        for tag in soup.find_all("a", attrs={'data-result-type': 'ResCard_Name'}):
            # if str(tag['href'].encode('utf-8').strip()) not in  out_file.read().replace('\n', '').encode('utf-8').strip() :   
                out_file.write(tag['href'].encode('utf-8').strip() + b'\n')
        
class ZomatoRestaurant:
    def __init__(self, url):
        self.url = url
       
        self.html_text = None
        try:
            browser.get(self.url)
            time.sleep(5)
            self.html_text = browser.page_source


        except Exception as err:
            print(str(err))
            return
        else:
            print('Access successful.')

        self.soup = None
        if self.html_text is not None:
            
            self.soup = BeautifulSoup(self.html_text, 'lxml')

    def scrap_rest_menu(self):
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
                dish_detail['Image-URLs'] = list()
                trim = re.compile(r'[^\d.,]+')
                dish_detail['dish_name'] = child_div_dish_name.text.strip() 
                dish_detail['dish_price'] = trim.sub('',child_div_dish_price.text.strip())
                menu_details['dish_mappings'].append(dish_detail)
                response = google_images_download.googleimagesdownload()   
                item = child_div_dish_name.text.strip()
                arguments = {"keywords": item ,"limit":1 ,"print_urls":True}  
                paths = response.download(arguments)   
                dish_detail['Image-URLs'].append(paths)  
        return menu_details
        
    def scrap_rest_detail(self):
        if self.soup is None:
            return {}
        soup = self.soup
        rest_details = dict()

        name_anchor = soup.find("a", attrs={"class": "ui large header left"})
        if name_anchor:
            rest_details['name'] = name_anchor.text.strip()
        else:
            rest_details['name'] = ''

        rating_div = soup.find("div", attrs={"class": re.compile("rating-for")})
        if rating_div:
            rest_details['rating'] = rating_div.text.strip()[:-2]
        else:
            rest_details['rating'] = 'N'  # default

        contact_span = soup.find("span", attrs={"class": 'tel'})
        if contact_span:
            rest_details['contact'] = contact_span.text.strip()
        else:
            rest_details['contact'] = ''

        cuisine_box = soup.find('div', attrs={'class': 'res-info-cuisines clearfix'})
        rest_details['cuisines'] = []
        if cuisine_box:
            for it in cuisine_box.find_all('a', attrs={'class': 'zred'}):
                rest_details['cuisines'].append(it.text)

        geo_locale = soup.find("div", attrs={"class": "resmap-img"})
        if geo_locale:
            geo_url = geo_locale.attrs['data-url']
            parsed_url = urlparse(geo_url)
            geo_arr = str(urllib.parse.parse_qs(parsed_url.query)['center']).split(',')
            rest_details['geo_location'] = [re.sub("[^0-9\.]", "", geo_arr[0]), re.sub("[^0-9\.]", "", geo_arr[1])]
        if 'geo_location' not in rest_details:
            rest_details['geo_location'] = ['undefined', 'undefined']

        price_two_tag = soup.find('div', attrs={'class': 'res-info-detail'})
        if price_two_tag:
            price_two_tag = price_two_tag.find('span', attrs={'tabindex': '0'})
        if price_two_tag:
            rest_details['price_two'] = re.sub("[^0-9]", "", price_two_tag.text.strip())

        price_beer_tag = soup.find('div', attrs={'class': 'res-info-detail'})
        if price_beer_tag:
            price_beer_tag = price_beer_tag.find('div', attrs={'class': 'mt5'})
        if price_beer_tag:
            rest_details['price_beer'] = re.sub("[^0-9]", "", price_beer_tag.text.strip())

        res_info = []
        for it in soup.findAll("div", attrs={'class': 'res-info-feature-text'}):
            try:
                res_info.append(it.text.strip())
            except NavigableString:
                pass
        rest_details['facility'] = res_info

        week_schedule = soup.find("div", attrs={"id": "res-week-timetable"})
        data = []
        if week_schedule:
            time_table = week_schedule.table
            rows = time_table.findAll('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
        rest_details['timetable'] = data

        collection_box = soup.find('div', attrs={'class': 'ln24'})
        rest_details['featured_collections'] = []
        if collection_box:
            for it in collection_box.find_all('a', attrs={'class': 'zred'}):
                rest_details['featured_collections'].append(it.text.strip())

        address_div = soup.find("div", attrs={"class": "resinfo-icon"})
        if address_div:
            rest_details['address'] = address_div.span.get_text()
        else:
            rest_details['address'] = ""

        known_for_div = soup.find("div", attrs={'class': 'res-info-known-for-text mr5'})
        if known_for_div:
            rest_details['known_for'] = known_for_div.text.strip()
        else:
            rest_details['known_for'] = ''

        rest_details['what_people_love_here'] = []
        for div in soup.find_all("div", attrs={'class': 'rv_highlights__section pr10'}):
            child_div = div.find("div", attrs={'class': 'grey-text'})
            if child_div:
                rest_details['what_people_love_here'].append(child_div.get_text())
        return rest_details

if __name__ == '__main__':
    if browser is None:
        print("Selenium not opened")
        sys.exit()

    for x in range(1, 53):
        print(str(x) + '\n')
        zr = ZomatoRestaurantLinkGen('https://www.zomato.com/indore/restaurants?page={}'.format(x))
        zr.scrap_rest_links()
    out_file.close()

    out_file = open("zomato_indore.json", "a")
    with open('Indore_restaurant_links.txt', 'r', encoding="utf-8") as f:
        for line in f:
            zr = ZomatoRestaurant(line) 
            json.dump(zr.scrap_rest_detail(), out_file)
            out_file.write('\n')
    out_file.close()
       
    out_file = open("zomato_menu.json", "a")
    with open("Indore_restaurant_links.txt", "r", encoding="utf-8") as f:
        for line in f:
            zr = ZomatoRestaurant(line + '/order')
            json.dump(zr.scrap_rest_menu(), out_file)
            out_file.write('\n')
    out_file.close()

    with open("Indore_restaurant_links.txt", "r", encoding="utf-8") as f:
        for line in f:
            img = Image_finder(line +'/menu#tabtop')
            img.scrap_image()
















    
