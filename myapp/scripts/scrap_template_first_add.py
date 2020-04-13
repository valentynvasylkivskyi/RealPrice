# SCRAP FIRST ADD TEMPLATE #
import os
import django
from datetime import datetime

from myapp.models import Shop, Product
from mysite.settings import MEDIA_ROOT
from .scrapers import scrap_allo, scrap_citrus, scrap_rozetka

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

        # update database fields
        product.now_price = data['product_price']
        product.min_price = data['product_price']
        product.max_price = data['product_price']
        product.product_name = data['product_name']

        # update field Last update
        now = datetime.now()
        product.last_update = now.strftime("%Y-%m-%d %H:%M:%S")

        # download image and add to image path
        filename = wget.download(data['product_image_link'])
        os.rename(filename, os.path.join(download_path, filename))
        product.product_image = 'images/{}'.format(filename)

        product.operation_result = True
        product.save()
    except:
        product.operation_result = False
        product.save()










