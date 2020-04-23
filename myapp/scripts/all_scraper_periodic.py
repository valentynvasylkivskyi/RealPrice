
# SCRAP PERIODIC TEMPLATE #
import os
import django
from django.utils import timezone
from time import sleep
from random import randint

from myapp.models import Product
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
            if product.last_price() != data['product_price']:
                product.price_set.create(price=data['product_price'])
            # update field Last update
            product.last_update = timezone.now()
            product.save()
        except:
            product.operation_result = False
            product.save()
            continue



















