from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import views
#from django.views.decorators.cache import cache_page


urlpatterns = [
    path(r'', views.ProductsListView.as_view(), name='home'),
    path('my_tracking', views.MyTrackingView.as_view(), name='my_tracking'),
    path('about', views.AboutView.as_view(), name='about'),
    path('about_as', views.AboutAsView.as_view(), name='about_as'),
    path('policy', views.PolicyView.as_view(), name='policy'),
    path('help', views.HelpView.as_view(), name='help'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('search', views.SearchView.as_view(), name='base_search_content'),
    path('add_tracking', views.AddTrackingView.as_view(), name='base_add_tracking'),
    path('prices_chart/<int:pk>/', views.product_prices_chart, name='prices_chart'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns


