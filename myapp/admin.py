from django.contrib import admin
from .models import Product, Shop, Price


#admin.site.register(Product)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name',
        'link',
        'shop',
        'visibility_status',
        'operation_result',
        'status',
        'last_update',
    )

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = (
                    'shop_name',
                    'id',
                    )

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'price',
        'date',
    )
