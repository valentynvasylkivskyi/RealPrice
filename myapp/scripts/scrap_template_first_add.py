# SCRAP FIRST ADD TEMPLATE #
import os
import django
from django.utils import timezone
import uuid
import requests
from user_agent import generate_user_agent

from myapp.models import Shop, Product, Price
from mysite.settings import MEDIA_ROOT
from .scrapers import scrap_allo, scrap_citrus, scrap_rozetka, scrap_comfy

import wget

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
dir = os.path.abspath(os.path.dirname(__file__))
download_path = MEDIA_ROOT + '/images/'

def scrap_template_first_add(product_id):
    product = Product.objects.get(id=product_id)
    try:
        if "allo.ua" in product.link:
            data = scrap_allo(product.link)
            if product.operation_result == False:
                product.shop = Shop.objects.get(shop_name='allo.ua')
        elif "rozetka.com.ua" in product.link:
            data = scrap_rozetka(product.link)
            if product.operation_result == False:
                product.shop = Shop.objects.get(shop_name='rozetka.com.ua')
        elif "citrus.ua" in product.link:
            data = scrap_citrus(product.link)
            if product.operation_result == False:
                product.shop = Shop.objects.get(shop_name='citrus.ua')
        elif "comfy.ua" in product.link:
            data = scrap_comfy(product.link)
            if product.operation_result == False:
                product.shop = Shop.objects.get(shop_name='comfy.ua')

        # update database fields
        product.price_set.create(price=data['product_price'])
        product.product_name = data['product_name']

        # update field Last update
        product.last_update = timezone.now()

        # download image and add to image path with WGET or requests
        random_name = uuid.uuid1()
        try:
            image = wget.download(data['product_image_link'])
            os.rename(image, os.path.join(download_path, "{}.jpg".format(random_name)))
            product.product_image = 'images/{}.jpg'.format(random_name)
        except:
            r = requests.get(data['product_image_link'], headers={'User-Agent': generate_user_agent()})
            with open(os.path.join(download_path, "{}.jpg".format(random_name)), 'wb') as f:
                f.write(r.content)
            product.product_image = 'images/{}.jpg'.format(random_name)

        product.operation_result = True
        product.save()
    except:
        product.operation_result = False
        product.save()










