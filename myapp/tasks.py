from mysite.celery import app

from myapp.models import Product
from .scripts.scrap_template_first_add import scrap_template_first_add
from .scripts.scrap_template_periodic import scrap_template_periodic


@app.task()
def add_product_task(product_id):
    scrap_template_first_add(product_id)
    return "One product add complete"

@app.task()
def scrap_rozetka_periodic():
    scrap_template_periodic('rozetka.com.ua')
    return "Periodic task scrap ROZETKA complete"

@app.task()
def scrap_citrus_periodic():
    scrap_template_periodic('citrus.ua')
    return "Periodic task scrap CITRUS complete"

@app.task()
def scrap_allo_periodic():
    scrap_template_periodic('allo.ua')
    return "Periodic task scrap ALLO complete"

