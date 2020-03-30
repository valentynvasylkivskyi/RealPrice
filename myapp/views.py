from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q


from .models import Product
from .forms import SignUpForm
from .tasks import gen_prime

from time import sleep


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

def product_list(request):
    if request.user.is_authenticated:
        auth_user = request.user.username
        products = Product.objects.filter(users__username__contains=auth_user)
        return render(request, 'myapp/product_list.html', {'products': products})
    else:
        return HttpResponseRedirect(reverse('login'))

def product_detail(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
    return render(request, 'myapp/product_detail.html', {'product': product})

def base(request):
    products_base = Product.objects.all()
    auth_user = request.user
    return render(request, 'myapp/base.html', {'user': auth_user, 'products_base': products_base})

def add_tracking_link(request):
    if request.user.is_authenticated:
        return  render(request, 'myapp/add_tracking.html')
    else:
        return HttpResponseRedirect(reverse('login'))

def add_tracking(request):
    auth_user = request.user
    link = request.GET.get('q')
    p = Product(link=link)
    p.save()
    p.users.add(auth_user)
    return HttpResponseRedirect(reverse('product_list'))

def test(request):
    primes = gen_prime.delay(100)
    sleep(5)
    if primes.ready():
        return HttpResponse('<h1>{}</h1>'.format(primes.get()))
    else:
        return HttpResponse('<h1>{}</h1>'.format('BAD BAD BAD'))








