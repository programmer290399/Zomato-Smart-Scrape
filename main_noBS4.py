import os 
import re
import sys
import time
import json
import urllib
import urllib.request
from urllib import parse
from random import randint
from selenium import webdriver
from urllib.parse import urlparse
from selenium.common import exceptions  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from google_images_download import google_images_download 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException








class Image_finder:
    def __init__(self, url):
        self.url = url
        
        
        try:
            browser.get(self.url)
            time.sleep(5)
        except Exception as err:
            print(str(err))
            return
        else:
            print('Sucessfully Accessed :' , self.url)
    
    
    
    def scrap_image(self):
    
        # soup.find("a",attrs={"class":"ui large header left"})
        rest_name = browser.find_element_by_xpath('//a[@class="ui large header left"]').text.strip()
        
        menu_image_URLs = dict()        
        menu_image_URLs[rest_name] = list()
        
        # list_len = soup.find('div', attrs={'class': 'pagination-meta left'})
        list_len = int(browser.find_element_by_xpath('//div[@class="pagination-meta left"]').text.strip().split()[3]) + 1
        for i in range(1,list_len):
            

            

            # div = soup.find('div', attrs={"id":"menu-image"})
            # div.find('img')
            image_link = str(browser.find_element_by_xpath('//div[@id="menu-image"]//child::img').get_attribute('src'))    
            menu_image_URLs[rest_name].append(image_link)
            time.sleep(5)
            wait = WebDriverWait(browser , 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-next-page"]')))
            element.click()
        return menu_image_URLs

class ZomatoRestaurantLinkGen:
    def __init__(self, url):
        self.url = url
        
        try:
            browser.get(self.url)
            

        except Exception as err:
            print(str(err))
            return
        else:
            print('Sucessfully Accessed :' , self.url )



    def scrap_rest_links(self):
        
        try :
            anchor_tags = browser.find_elements_by_xpath('//a[@data-result-type="ResCard_Name"]') 
        except :
            pass
        
        try :
            anchor_tags_minor = browser.find_elements_by_xpath('//a[@class="ui col-l-16 search_chain_bottom_snippet"]')
        except :
            pass
        
        anchor_pool = anchor_tags + anchor_tags_minor
        
        for tag in anchor_pool  :
                out_file.write(tag.get_attribute('href').encode('utf-8').strip() + b'\n')
        
class ZomatoRestaurant:
    def __init__(self, url):
        self.url = url
    
        
        try:
            browser.get(self.url)
            time.sleep(5)
            


        except Exception as err:
            print(str(err))
            return
        else:
            print('Sucessfully Accessed :' , self.url)


    def scrap_rest_menu(self):
        
        trim = re.compile(r'[^\d.,]+')
        menu_details = dict()
        
        try:
            # soup.find('a', attrs={'class': 'o2header-title'})
            name_anchor = browser.find_element_by_xpath('//a[@class="o2header-title"]')
            menu_details['restaurant_name'] = name_anchor.text.strip()
        except :
            return {'Message':'This restaurant has no orders page'}
        
        dish_mappings = list()
        
        try :
                dishes = browser.find_elements_by_xpath('//div[@class="col-s-10 col-m-13"]')
                for dish in dishes :
                    dish_detail = dict()
                    dish_type = {'veg':False , 'non_veg':False , 'Other':False}
                    try:
                        dish_name = dish.find_element_by_xpath('.//div[@class="header"]')
                        dish_detail['dish_name'] = dish_name.text.strip()
                        # Uncomment this part to download images .....
                        # response = google_images_download.googleimagesdownload()   
                        # item = dish_name.text.strip()
                        # arguments = {"keywords": item ,"limit":1 ,"print_urls":True}  
                        # paths = response.download(arguments)   
                        # dish_detail['Image-URLs'].append(paths)
                    except :
                        pass
                    try :
                        dish_price = dish.find_element_by_xpath('.//div[@class="description"]')
                        dish_detail['dish_price'] = trim.sub('', dish_price.text.strip())
                    except :
                        pass
                    try :
                        dish_type_test = dish.find_element_by_xpath('.//div[@class="veg tag left"]')
                        dish_type['veg'] = True
                    except :
                        try :
                            dish_type_test = dish.find_element_by_xpath('.//div[@class="nveg tag left"]')
                            dish_type['non_veg'] = True 
                        except :
                            dish_type['Other'] = True 
                    if dish_type['veg'] : dish_detail['type'] = 'Veg'
                    elif dish_type['non_veg'] : dish_detail['type'] = 'Non-veg'
                    elif dish_type['Other'] : dish_detail['type'] = 'Not Specified'
                    
                    try :
                        dish_category = dish.find_element_by_xpath('.//ancestor::div[@class="ui divided items mbot0 category"]//preceding-sibling::div[@class="category_heading"]')
                        dish_detail['Category'] = dish_category.text.strip()
                    except :
                        
                        try :
                            sub_category = dish.find_element_by_xpath('./ancestor::div[@class="ui segment category-container"]/h3')
                            dish_detail['Category'] = sub_category.text.strip()
                        except:
                            pass 
                    dish_mappings.append(dish_detail) 
        except :
            return 
        menu_details['dish_mappings'] = dish_mappings
        return menu_details
    
    def scrap_rest_detail(self):

        rest_details = dict()

        
        try :
            # soup.find("a", attrs={"class": "ui large header left"})
            name_anchor = browser.find_element_by_xpath('//a[@class="ui large header left"]')
            rest_details['name'] = name_anchor.text.strip()
            print('fetched restaurant name ...')
        except :
            return 

        try :
            # soup.find("div", attrs={"class": re.compile("rating-for")})
            rating_div = browser.find_element_by_xpath('//div[starts-with(@class,"rating-for")]')
            rest_details['rating'] = rating_div.text.strip()[:-2]
            print('fetched restaurant rating ...')
        except:
            rest_details['rating'] = 'None'  # default
        
        try :
            # soup.find("span", attrs={"class": 'tel'})
            contact_numbers = list()
            contact_spans = browser.find_elements_by_xpath('//span[@class="tel"]')
            for number in contact_spans :
                contact_numbers.append(number.text.strip())
            rest_details['contact'] = contact_numbers
            print('fetched restaurant contacts ...')
        except :
            pass 

            # soup.find('div', attrs={'class': 'res-info-cuisines clearfix'})
            # find_all('a', attrs={'class': 'zred'}):
        rest_details['cuisines'] = list()
        try :    
            cuisine_box = browser.find_elements_by_xpath('//div[@class="res-info-cuisines clearfix"]//child::a[@class="zred"]')
            for it in cuisine_box :
                rest_details['cuisines'].append(it.text)
            print('fetched restaurant cuisines ...')
        except :
            pass 
        # soup.find("div", attrs={"class": "resmap-img"})
        try :
            geo_locale = browser.find_element_by_xpath('//div[@class="resmap-img"]')
            geo_url = geo_locale.get_attribute('data-url')
            parsed_url = urlparse(geo_url)
            geo_arr = str(urllib.parse.parse_qs(parsed_url.query)['center']).split(',')
            rest_details['geo_location'] = [re.sub("[^0-9\.]", "", geo_arr[0]), re.sub("[^0-9\.]", "", geo_arr[1])]
            print('fetched restaurant geo location  ...')
        except :
            pass 
        
        try :
            # soup.find('div', attrs={'class': 'res-info-detail'})
            # price_two_tag = price_two_tag.find('span', attrs={'tabindex': '0'})
            price_two_tag = browser.find_element_by_xpath('//div[@class="res-info-detail"]//child::span[@tabindex="0"]') 
            rest_details['price_two'] = re.sub("[^0-9]", "", price_two_tag.text.strip())
            print('fetched restaurant price for two  ...')
        except :
            pass 
            
        try :
            # soup.find('div', attrs={'class': 'res-info-detail'})
            # price_beer_tag = price_beer_tag.find('div', attrs={'class': 'mt5'})
            price_beer_tag = browser.find_element_by_xpath('//div[@class="res-info-detail"]//child::div[@class="mt5"]')
            rest_details['price_beer'] = re.sub("[^0-9]", "", price_beer_tag.text.strip())
            print('fetched restaurant beer price ...')
        except :
            pass 

        try :
            res_info = list() 
            # soup.findAll("div", attrs={'class': 'res-info-feature-text'})
            features = browser.find_elements_by_xpath('//div[@class="res-info-feature-text"]')
            for it in features:
                try:
                    res_info.append(it.text.strip())
                except :
                    pass
            rest_details['facility'] = res_info
            print('fetched restaurant facilities ...')
        except :
            pass 
        
        
        # soup.find("div", attrs={"id": "res-week-timetable"})
        try :
            data = list()
            time_table =  browser.find_element_by_xpath('//div[@id="res-week-timetable"]//child::table')
            rows = time_table.find_elements_by_tagname('tr')
            for row in rows:
                cols = row.find_elements_by_tagname('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
            rest_details['timetable'] = data
            print('fetched restaurant time table ...')
        except :
            pass 
        try :
            # soup.find('div', attrs={'class': 'ln24'}).find_all('a', attrs={'class': 'zred'})
            collection_box = browser.find_elements_by_xpath('//div[@class="ln24"]//child::a[@class="zred"]')
            rest_details['featured_collections'] = list()
            for it in collection_box :
                rest_details['featured_collections'].append(it.text.strip())
            print('fetched restaurant featured collection ...')
        except :
            pass
        
        try :
            # soup.find("div", attrs={"class": "resinfo-icon"})
            address_div = browser.find_element_by_xpath('//div[@class="resinfo-icon"]') 
            rest_details['address'] = address_div.text
            print('fetched restaurant address ...')
        except :
            pass 
            
        try :
            # soup.find("div", attrs={'class': 'res-info-known-for-text mr5'})
            known_for_div = browser.find_element_by_xpath('//div[@class="res-info-known-for-text mr5"]')
            rest_details['known_for'] = known_for_div.text.strip()
            print('fetched restaurant speciality  ...')
        except :
            pass 
        
        
        
        # soup.find_all("div", attrs={'class': 'rv_highlights__section pr10'}):
        # child_div = div.find("div", attrs={'class': 'grey-text'})
        try :
            rest_details['what_people_love_here'] = []
            what_people_love_here = browser.find_elements_by_xpath('//div[@class="rv_highlights__section pr10"]//child::div[@class="grey-text"]')
            for div in  what_people_love_here :
                    rest_details['what_people_love_here'].append(div.text)
            print('fetched restaurant popularity ...')
        except :
            pass  
        return rest_details






if __name__ == '__main__':
    
    # Taking Control of the browser ....
    browser = None
    try:
        browser = webdriver.Chrome()
    except Exception as error:
        print(error)

    if browser is None:
        print("Selenium not opened")
        sys.exit()


    # Getting links of resturant pages .....
    with open("Indore_restaurant_links.txt", "wb+") as out_file :
        browser.get('https://www.zomato.com/indore/restaurants?page=1')
        num_of_pages = int(browser.find_element_by_xpath('//div[@class="col-l-4 mtop pagination-number"]//child::div').text.split()[3]) + 1
        
        for x in range(1, num_of_pages):
            print(str(x)+ "/{} pages done".format(num_of_pages) + '\n')
            zr = ZomatoRestaurantLinkGen('https://www.zomato.com/indore/restaurants?page={}'.format(x))
            zr.scrap_rest_links()
    out_file.close()
    
    # Scrapping details about the restaurant .....
    out_file = open("zomato_indore.json", "a")
    with open('Indore_restaurant_links.txt', 'r', encoding="utf-8") as f:
        for line in f:
            zr = ZomatoRestaurant(line) 
            json.dump(zr.scrap_rest_detail(), out_file)
            out_file.write('\n')
    out_file.close()
    
    # Scraping menu ....
    out_file = open("zomato_menu.json", "a")
    with open("Indore_restaurant_links.txt", "r", encoding="utf-8") as f:
        for line in f:
            zr = ZomatoRestaurant(line + '/order')
            json.dump(zr.scrap_rest_menu(), out_file)
            out_file.write('\n')
    out_file.close()

    # Scrapping menu image links  .....
    out_file = open("zomato_menu_image_links.json", "a")
    with open("Indore_restaurant_links.txt", "r", encoding="utf-8") as f:
        for line in f:
            img = Image_finder(line +'/menu#tabtop')
            json.dump(img.scrap_image(), out_file)
            out_file.write('\n')
    out_file.close()
    browser.close()
















    
