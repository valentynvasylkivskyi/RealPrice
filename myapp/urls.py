from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('product_list', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.base, name='home'),
    path('signup/', views.signup, name='signup'),
    path('search/', views.search, name='search_result'),

]

