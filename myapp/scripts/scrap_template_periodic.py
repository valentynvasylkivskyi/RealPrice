
# SCRAP PERIODIC TEMPLATE #
import os
import django
from time import sleep
from random import randint
from datetime import datetime

from myapp.models import Product, Shop
from mysite.settings import MEDIA_ROOT
from .scrapers import scrap_allo, scrap_citrus, scrap_rozetka

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
dir = os.path.abspath(os.path.dirname(__file__))
download_path = MEDIA_ROOT + '/images/'

def random_sleep(start=1, end=3):
    sleep(randint(start, end))

def product_update_fields(product, data):
    product_price = data['product_price']

    # update database fields
    product.now_price = product_price
    if product.min_price > product_price:
        product.min_price = product_price
    if product.max_price < product_price:
        product.max_price = product_price

    # update field Last update
    now = datetime.now()
    product.last_update = now.strftime("%Y-%m-%d %H:%M:%S")

    product.operation_result = True
    product.save()

def scrap_template_periodic(shop):
    shop_id = Shop.objects.get(shop_name=shop).id
    products = Product.objects.filter(shop=shop_id)
    if shop == "citrus.ua":
        for product in products:
            try:
                random_sleep()
                data = scrap_citrus(product.link)
                product_update_fields(product, data)
            except:
                product.operation_result = False
                product.save()
                continue
    elif shop == "allo.ua":
        for product in products:
            try:
                random_sleep()
                data = scrap_allo(product.link)
                product_update_fields(product, data)
            except:
                product.operation_result = False
                product.save()
    elif shop == "rozetka.com.ua":
        for product in products:
            try:
                random_sleep()
                data = scrap_rozetka(product.link)
                product_update_fields(product, data)
            except:
                product.operation_result = False
                product.save()


















