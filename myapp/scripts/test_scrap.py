# Scrap URL from test shop #

import os

from time import sleep
from random import randint
from datetime import datetime


from bs4 import BeautifulSoup
import requests
import wget
from user_agent import generate_user_agent


dir = os.path.abspath(os.path.dirname(__file__))
download_path = r"C:\Users\vasilkovskiy\Downloads\images"

def random_sleep(start=1, end=3):
    sleep(randint(start, end))

link = "https://www.citrus.ua/smartfony/iphone-xr-apple-632724.html"

def scrap_citrus_script():
    try:
        random_sleep()
        headers = {'User-Agent': generate_user_agent()}

        data_source = requests.get(link, headers)

        soup = BeautifulSoup(data_source.text, "html.parser")

        # get product fields
        product_name = soup.find("header", class_="product__header").find("h1").text
        price = soup.find("div", class_="normal__prices").find_all("div")
        for i in price:
            if '<div class="price"' in str(i):
                price = i.find("span").text

        # get image source
        image_source = requests.get(link+"?tab=photo")
        soup = BeautifulSoup(image_source.text, "html.parser")
        product_image_link = soup.find("ul", class_="gallery").find("li").find("img").get('src')

        product_price = ''
        for i in price:
            if str(i).isnumeric():
                product_price += i

        product_price = int(product_price)

        print(product_name,'\n', price,'\n', product_image_link)


        #filename = wget.download(product_image_link)
        #os.rename(filename, os.path.join(download_path, filename))
        #product_image = 'images/{}'.format(filename)
    except:
        print("rrr")


scrap_citrus_script()


















