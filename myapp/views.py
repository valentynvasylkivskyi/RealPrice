from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q
from django.views.generic import ListView

from .models import Product
from .forms import SignUpForm
from .tasks import add_product_task

class ProductsListView(ListView):
    model = Product
    template_name = 'myapp/base.html'
    paginate_by = 12
    context_object_name = "products"
    queryset = Product.objects.filter(operation_result=True)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(min_price__icontains=query) |
            Q(now_price__icontains=query) |
            Q(max_price__icontains=query)
        )
    return render(request, 'myapp/base_search_content.html', {'products': products})

def my_tracking(request):
    if request.user.is_authenticated:
        auth_user = request.user.username
        products = Product.objects.filter(users__username__contains=auth_user, operation_result=True)
        return render(request, 'myapp/base_my_tracking.html', {'products': products})
    else:
        return HttpResponseRedirect(reverse('login'))

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
















