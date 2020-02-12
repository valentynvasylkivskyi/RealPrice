from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Product(models.Model):
    users = models.ManyToManyField(User)
    product_name = models.CharField(max_length=256, null=False, blank=True)
    min_price = models.IntegerField()
    now_price = models.IntegerField()
    max_price = models.IntegerField()
    link = models.CharField(max_length=1024, null=False, blank=True)
    product_image = models.ImageField(upload_to='images', default='../media/images/default_img.jpg')

    def __str__(self):
        return self.product_name











