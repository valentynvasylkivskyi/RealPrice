from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Prefetch
from django.views.generic import View
from braces.views import LoginRequiredMixin
from django_filters.views import FilterView

from .models import Product, Price
from .forms import SignUpForm
from .filters import ProductFilter
from .scripts.scrap_template_first_add import scrap_template_first_add

class ProductsListView(FilterView):
    model = Product
    template_name = 'myapp/base.html'
    paginate_by = 15
    filterset_class = ProductFilter
    context_object_name = 'filter'

    def get_queryset(self):
        queryset = ProductFilter(
            self.request.GET,
            Product.objects.prefetch_related(
                Prefetch('prices', queryset=Price.objects.order_by('date'), to_attr='prices_ASC'),
                Prefetch('prices', queryset=Price.objects.order_by('-date'), to_attr='prices_DESC'),
                ).order_by('id').filter(operation_result=True).distinct()
        ).qs
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

















