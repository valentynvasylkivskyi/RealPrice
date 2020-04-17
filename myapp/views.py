from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q


from .models import Product, Shop
from .forms import SignUpForm
from .tasks import add_product_task


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
    search_result = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(min_price__icontains=query) |
            Q(now_price__icontains=query) |
            Q(max_price__icontains=query)
        )
    return render(request, 'myapp/search_result.html', {'search_result': search_result})

def my_tracking(request):
    if request.user.is_authenticated:
        auth_user = request.user.username
        products = Product.objects.filter(users__username__contains=auth_user)
        shops = Shop.objects.all()
        return render(request, 'myapp/my_tracking.html', {'products': products, 'shops': shops})
    else:
        return HttpResponseRedirect(reverse('login'))


def base(request):
    products_base = Product.objects.all()
    shops = Shop.objects.all()
    auth_user = request.user
    return render(request, 'myapp/base.html', {'user': auth_user, 'products_base': products_base, 'shops': shops})

def add_tracking_link(request):
    if request.user.is_authenticated:
        return  render(request, 'myapp/add_tracking.html')
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

def all_trackers_by_shops(request, shop_name):
    products = Product.objects.filter(shop=Shop.objects.get(shop_name=shop_name).id)
    shops = Shop.objects.all()
    return render(request, 'myapp/shops.html', {'products': products, 'shops': shops})

def my_trackers_by_shops(request, shop_name):
    products = Product.objects.filter(shop=Shop.objects.get(shop_name=shop_name).id, users__username__contains=request.user.username)
    shops = Shop.objects.all()
    return render(request, 'myapp/products_by_shop.html', {'products': products, 'shops': shops})












