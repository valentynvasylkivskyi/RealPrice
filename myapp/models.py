from django.contrib.auth.models import User
from django.db import models


DEFAULT_PRODUCT_NAME = 'Wait robot tracking'
DEFAULT_IMAGE_PATH = '../media/images/default_img.jpg'
DEFAULT_SHOP_ID = 1 # id = 1, shop_name = New products without shop
DEFAULT_VISIBILITY_STATUS = 1

class Shop(models.Model):
    shop_name = models.CharField(max_length=64, null=False)

    def __str__(self):
        return self.shop_name

class Product(models.Model):
    public_visibility = 1
    private_visibility = 2
    visibility = (
        (public_visibility, 'public'),
        (private_visibility, 'private'),
    )
    users = models.ManyToManyField(User)
    product_name = models.CharField(max_length=256, default=DEFAULT_PRODUCT_NAME)
    min_price = models.IntegerField(default=0)
    now_price = models.IntegerField(default=0)
    max_price = models.IntegerField(default=0)
    link = models.CharField(max_length=1024, null=False, blank=True)
    product_image = models.ImageField(upload_to='images', default=DEFAULT_IMAGE_PATH)

    # Before import shop foreignkey add default shop to the shop table
    #shop = models.ForeignKey(Shop, on_delete=models.CASCADE, default=DEFAULT_SHOP_ID)


    visibility_status = models.PositiveSmallIntegerField(choices=visibility, default=DEFAULT_VISIBILITY_STATUS)

    # Robot tracking result (True/False)
    operation_result = models.BooleanField(default=False)

    # Status of products (disabled = False / enabled = True)
    status = models.BooleanField(default=True)

    last_update = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.product_name











