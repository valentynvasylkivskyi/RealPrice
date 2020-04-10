# Scrap URL from citrus.ua shop #

import os
import django
from time import sleep
from random import randint
from datetime import datetime

from myapp.models import Shop
from mysite.settings import MEDIA_ROOT

from bs4 import BeautifulSoup
import requests
import wget
from user_agent import generate_user_agent

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
dir = os.path.abspath(os.path.dirname(__file__))
download_path = MEDIA_ROOT + '/images/'

def random_sleep(start=1, end=3):
    sleep(randint(start, end))

def scrap_citrus_script(products):
    for product in products:
        try:
            random_sleep()
            headers = {'User-Agent': generate_user_agent()}

            data_source = requests.get(product.link, headers)

            soup = BeautifulSoup(data_source.text, "html.parser")

            # get product fields
            product_name = soup.find("header", class_="product__header").find("h1").text
            price = soup.find("div", class_="normal__prices").find_all("div")
            for i in price:
                if '<div class="price"' in str(i):
                    price = i.find("span").text

            # get image source
            image_source = requests.get(product.link+"?tab=photo")
            soup = BeautifulSoup(image_source.text, "html.parser")
            product_image_link = soup.find("ul", class_="gallery").find("li").find("img").get('src')

            product_price = ''
            for i in price:
                if str(i).isnumeric():
                    product_price += i

            product_price = int(product_price)

            # update database fields
            product.now_price = product_price
            if product.min_price > product_price or product.min_price == 0:
                product.min_price = product_price
            if product.max_price < product_price or product.max_price == 0:
                product.max_price = product_price

            if product.product_name == 'Wait robot tracking':
                product.product_name = product_name

            # update field Last update
            now = datetime.now()
            product.last_update = now.strftime("%Y-%m-%d %H:%M:%S")



            # TODO check image path in image storage
            if product.operation_result == False:
                filename = wget.download(product_image_link)
                os.rename(filename, os.path.join(download_path, filename))
                product.product_image = 'images/{}'.format(filename)

                shop = Shop.objects.get(shop_name='citrus.ua')
                product.shop = shop

            product.operation_result = True
            product.save()
        except:
            product.operation_result = False
            product.save()
            continue









