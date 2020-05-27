from django import forms
from .models import Product, Shop
import django_filters

class ProductFilter(django_filters.FilterSet):
    shop = django_filters.ModelMultipleChoiceFilter(
        queryset=Shop.objects.all(),
        widget = forms.CheckboxSelectMultiple,
    )
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='prices__price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='prices__price', lookup_expr='lt')
    class Meta:
        model = Product
        fields = ['shop',]
