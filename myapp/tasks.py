from mysite.celery import app
from .models import Product
from django.contrib.auth.models import User



@app.task()
def add_tracking_task(link, uid):
    p = Product(link=link)
    p.save()
    user = User.objects.get(id=uid)
    p.users.add(user)
    return "the new product adding for {} complete".format(user.username)




