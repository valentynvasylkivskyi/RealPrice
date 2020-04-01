from mysite.celery import app

from myapp.models import Product
from .scripts.scrap_rozetka import scrap_rozetka_script


@app.task()
def add_product_task(product_id):
    if "rozetka.com.ua" in Product.objects.get(id=product_id).link:
        scrap_rozetka_script(Product.objects.filter(id=product_id))
    return "One product add complete"

@app.task()
def scrap_rozetka_periodic():
    # get all products from DB where 'rozetka.com.ua' in URL
    products = Product.objects.filter(link__contains='rozetka.com.ua')
    scrap_rozetka_script(products)
    return "Periodic task scrap rozetka complete"






