from mysite.celery import app

from myapp.models import Product
from .scripts.scrap_rozetka import scrap_rozetka_script
from .scripts.scrap_citrus import scrap_citrus_script
from .scripts.scrap_template import scrap_template


@app.task()
def add_product_task(product_id):
    link = Product.objects.get(id=product_id).link
    product = Product.objects.filter(id=product_id)

    if "rozetka.com.ua" in link:
        scrap_rozetka_script(product)
    elif "citrus.ua" in link:
        scrap_citrus_script(product)
    elif "allo.ua" in link:
        scrap_template(product)
    return "One product add complete"

@app.task()
def scrap_rozetka_periodic():
    # get all products from DB where 'rozetka.com.ua' in URL
    products = Product.objects.filter(link__contains='rozetka.com.ua')
    scrap_rozetka_script(products)
    return "Periodic task scrap ROZETKA complete"

@app.task()
def scrap_citrus_periodic():
    # get all products from DB where 'citrus.ua' in URL
    products = Product.objects.filter(link__contains='citrus.ua')
    scrap_citrus_script(products)
    return "Periodic task scrap CITRUS complete"


