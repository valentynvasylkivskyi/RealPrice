from django import forms
from .models import Product, Shop
import django_filters

CHOICES = (
    ('-created', 'новые'),
    ('discount', 'скидка по убыванию'),
    ('-discount', 'скидка по возрастанию'),
    ('current_price', 'по возрастанию цены'),
    ('-current_price', 'по убыванию цены'),

)
class ProductFilter(django_filters.FilterSet):
    shop = django_filters.ModelMultipleChoiceFilter(
        queryset=Shop.objects.all(),
        widget = forms.CheckboxSelectMultiple,
    )
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='current_price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='current_price', lookup_expr='lt')

    order = django_filters.OrderingFilter(
        choices=CHOICES,
        fields=(
            ('created', 'created'),
            ('discount', 'discount'),
            ('current_price', 'current_price'),
        ),
        empty_label=None,
    )
    class Meta:
        model = Product
        fields = ['shop', ]

