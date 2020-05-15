from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q, Prefetch
from django.views.generic import ListView, View
from braces.views import LoginRequiredMixin

from .models import Product, Price
from .forms import SignUpForm
from .tasks import add_product_task

class ProductsListView(ListView):
    model = Product
    template_name = 'myapp/base.html'
    paginate_by = 12
    context_object_name = "products"
    queryset = Product.objects.prefetch_related(
        Prefetch('prices', queryset=Price.objects.order_by('date'), to_attr='prices_ASC'),
        Prefetch('prices', queryset=Price.objects.order_by('-date'), to_attr='prices_DESC'),
    )

class MyTrackingView(LoginRequiredMixin, ProductsListView):
    login_url = 'login'

    def get_template_names(self):
        template_name = 'myapp/base_my_tracking.html'
        return template_name
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            users__username__contains=self.request.user.username,
            operation_result=True,
        )
        return queryset

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

def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(min_price__icontains=query) |
            Q(now_price__icontains=query) |
            Q(max_price__icontains=query)
        )
    return render(request, 'myapp/base_search_content.html', {'products': products})


def add_tracking_link(request):
    if request.user.is_authenticated:
        return  render(request, 'myapp/base_add_tracking.html')
    else:
        return HttpResponseRedirect(reverse('login'))

def add_tracking(request):
    user = request.user
    link = request.GET.get('q')
    p = Product(link=link)
    p.save()
    p.users.add(user)

    add_product_task.delay(p.id)
    return HttpResponseRedirect(reverse('my_tracking'))
















