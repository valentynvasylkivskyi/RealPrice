from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.ProductsListView.as_view(), name='home'),
    path('my_tracking', views.MyTrackingView.as_view(), name='my_tracking'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('search', views.search, name='base_search_content'),
    path('add_tracking', views.add_tracking_link, name='base_add_tracking'),
    path('add', views.add_tracking, name='add'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns


