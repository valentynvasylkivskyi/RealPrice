from mysite.celery import app
from .models import Product

from .scripts.scrap_template_first_add import scrap_template_first_add
from .scripts.all_scraper_periodic import all_scraper_periodic


@app.task()
def add_product_task(product_id):
    scrap_template_first_add(product_id)
    return "ADD COMPLETE"

@app.task()
def all_scraper_periodic_task():
    products = Product.objects.filter(operation_result=True, status=True)
    all_scraper_periodic(products)
    return "PERIODIC TASK COMPLETE"


