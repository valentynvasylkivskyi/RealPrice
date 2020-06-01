
# SCRAP PERIODIC TEMPLATE #
import os
import django
from django.utils import timezone
from time import sleep
from random import randint

from mysite.settings import MEDIA_ROOT
from . import scrapers

import tldextract

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
dir = os.path.abspath(os.path.dirname(__file__))
download_path = MEDIA_ROOT + '/images/'

def random_sleep(start=1, end=3):
    sleep(randint(start, end))


def all_scraper_periodic(products):
    for product in products:
        try:
            scraper = tldextract.extract(product.link).domain
            method_to_call = getattr(scrapers, scraper)
            random_sleep()
            data = method_to_call(product.link)
            # add price
            if product.current_price != data['product_price']:
                product.prices.create(price=data['product_price'])
                product.current_price = data['product_price']
            # update field Last update and discount
            product.last_update = timezone.now()
            product.discount = product.get_discount()
            product.operation_result = True
            product.save()
        except:
            product.operation_result = False
            product.save()
            continue



















