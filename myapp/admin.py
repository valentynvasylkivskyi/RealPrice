from django.contrib import admin
from .models import Product


#admin.site.register(Product)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', "min_price", "now_price", 'max_price', 'link',)

