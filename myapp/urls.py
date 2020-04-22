from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.ProductsListView.as_view(), name='home'),
    path('my_tracking', views.my_tracking, name='my_tracking'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('search', views.search, name='base_search_content'),
    path('add_tracking', views.add_tracking_link, name='base_add_tracking'),
    path('add', views.add_tracking, name='add'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


