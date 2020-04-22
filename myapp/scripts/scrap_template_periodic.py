
# SCRAP PERIODIC TEMPLATE #
import os
import django
from django.utils import timezone
from time import sleep
from random import randint
from datetime import datetime

from myapp.models import Product, Shop, Price
from mysite.settings import MEDIA_ROOT
from .scrapers import scrap_allo, scrap_citrus, scrap_rozetka, scrap_comfy

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
dir = os.path.abspath(os.path.dirname(__file__))
download_path = MEDIA_ROOT + '/images/'

def random_sleep(start=1, end=3):
    sleep(randint(start, end))

def product_update_fields(product, data):
    # add price
    if product.last_price() != data['product_price']:
        product.price_set.create(price=data['product_price'])

    # update field Last update
    product.last_update = timezone.now()

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
    elif shop == "comfy.ua":
        for product in products:
            try:
                random_sleep()
                data = scrap_comfy(product.link)
                product_update_fields(product, data)
            except:
                product.operation_result = False
                product.save()


















