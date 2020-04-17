from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('my_tracking', views.my_tracking, name='my_tracking'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.base, name='home'),
    path('signup/', views.signup, name='signup'),
    path('search', views.search, name='search_result'),
    path('add_tracking', views.add_tracking_link, name='add_tracking'),
    path('add', views.add_tracking, name='add'),
    path('shops/<str:shop_name>', views.all_trackers_by_shops, name='shops'),
    path('my_tracking/shops/<str:shop_name>', views.my_trackers_by_shops, name='products_by_shop'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


