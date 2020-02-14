from django.contrib import admin
from .models import Product, Shop


#admin.site.register(Product)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name',
        "min_price",
        "now_price",
        'max_price',
        'link',
        'shop',
        'visibility_status',
        'operation_result',
        'status',
        'last_update',
    )

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'shop_name',
                    )