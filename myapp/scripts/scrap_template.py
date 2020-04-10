# SCRAP TEMPLATE #
import os
import django
from time import sleep
from random import randint
from datetime import datetime

from myapp.models import Shop
from mysite.settings import MEDIA_ROOT
from .scrapers import scrap_allo

import wget
from user_agent import generate_user_agent

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
dir = os.path.abspath(os.path.dirname(__file__))
download_path = MEDIA_ROOT + '/images/'

def random_sleep(start=1, end=3):
    sleep(randint(start, end))

def scrap_template(products):
    for product in products:
        try:
            random_sleep()
            headers = {'User-Agent': generate_user_agent()}

            if "allo.ua" in product.link:
                data = scrap_allo(product.link, headers)
                if product.operation_result == False:
                    product.shop = Shop.objects.get(shop_name='allo.ua')

            product_name = data['product_name']
            product_price = data['product_price']
            product_image_link = data['product_image_link']

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

            product.operation_result = True
            product.save()
        except:
            product.operation_result = False
            product.save()
            continue









