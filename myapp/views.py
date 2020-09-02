from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Prefetch
from django.views.generic import View, TemplateView, ListView
from braces.views import LoginRequiredMixin
from django_filters.views import FilterView

import json

from .models import Product, Price, News
from .forms import SignUpForm
from .filters import ProductFilter
from .scripts.scrap_template_first_add import scrap_template_first_add


class ProductsListView(FilterView):
    model = Product
    template_name = 'myapp/base.html'
    paginate_by = 15
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = self.model.objects.filter(operation_result=True).prefetch_related(
                Prefetch('prices', queryset=Price.objects.order_by('date'), to_attr='prices_ASC'),
                Prefetch('prices', queryset=Price.objects.order_by('-date'), to_attr='prices_DESC'),
                ).order_by('-created')
        return queryset


class MyTrackingView(LoginRequiredMixin, ProductsListView):
    login_url = 'login'

    def get_template_names(self):
        template_name = 'myapp/base_my_tracking.html'
        return template_name
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            users__username__contains=self.request.user.username,
        )
        return queryset

class AboutView(TemplateView):
    template_name = 'myapp/about.html'

class AboutAsView(TemplateView):
    template_name = 'myapp/about_as.html'

class PolicyView(TemplateView):
    template_name = 'myapp/policy.html'

class HelpView(TemplateView):
    template_name = 'myapp/help.html'

class NewsView(ListView):
    model = News
    template_name = 'myapp/news.html'

    def get_queryset(self):
        queryset = self.model.objects.order_by('-date')
        return queryset

class RulesView(TemplateView):
    template_name = 'myapp/rules.html'

class SearchView(ProductsListView):

    def get_template_names(self):
        template_name = 'myapp/base_search_content.html'
        return template_name
    def get_queryset(self):
        url_parameters = self.request.GET.get('q')
        queryset = super().get_queryset().filter(
            product_name__icontains=url_parameters,
        )
        return queryset

class AddTrackingView(LoginRequiredMixin, ProductsListView):
    login_url = 'login'

    def get_template_names(self):
        template_name = 'myapp/base_add_tracking.html'
        return template_name
    def post(self, request):
        new_product = Product(link=request.POST.get('q'))
        new_product.save()
        new_product.users.add(self.request.user)
        scrap_template_first_add(new_product.id)
        return HttpResponseRedirect(reverse('my_tracking'))

class SignUpView(View):
    def render(self, request):
        return render(request, 'registration/signup.html', {'form': self.form})

    def post(self, request):
        self.form = SignUpForm(request.POST)
        if self.form.is_valid():
            self.form.save()
            username = self.form.cleaned_data.get('username')
            raw_password = self.form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        return self.render(request)

    def get(self, request):
        self.form = SignUpForm()
        return self.render(request)

def product_prices_chart(request, pk):
    product = Product.objects.get(id=pk)
    data_set = product.prices.order_by('date')

    categories = list()
    prices_data = list()

    for entry in data_set:
        categories.append(entry.date.strftime("%d/%m/%Y"))
        prices_data.append(entry.price)

    prices = {
        'name': 'Цена',
        'data': prices_data,
        'color': '#f92672'
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': '{}'.format(product.product_name)},
        'xAxis': {'categories': categories},
        'series': [prices]
    }
    dump = json.dumps(chart, indent=4, sort_keys=True, default=str)
    return render(request, 'myapp/product_prices_chart.html', {'chart': dump, 'prices': data_set})














