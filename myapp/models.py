from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Product(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    product_name = models.CharField(max_length=256, null=False, blank=True)
    min_price = models.IntegerField()
    now_price = models.IntegerField()
    max_price = models.IntegerField()
    link = models.CharField(max_length=1024, null=False, blank=True)
    product_image = models.ImageField(upload_to='images', default='../media/images/default_img.jpg')

    def __str__(self):
        return "Name: {} Price: {}".format(self.product_name, self.now_price)










