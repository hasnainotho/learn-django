from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token 


urlpatterns = [
    path('menu-items', views.MenuItemViews.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('category/<int:pk>', views.category_detail, name='category_detail'),
    path('items', views.get_items, name='items'),
    path('new-menu', views.menu, name='menu'),
    path('welcome', views.welcome),
    path('csv-render', views.csv_render),
    path('yaml-render', views.yaml_render),
    path('some-items', views.SomeItems.as_view({'get': 'list'})),
    path('some-items/<int:pk>', views.SomeItems.as_view({'get': 'retrieve'})),
    path('secret', views.some_secret),
    path('obtain-token-auth', obtain_auth_token),
    path('manager-view', views.manager_view),
    path('throttle-rate', views.throttle_view),
    path('test-cache', views.test_cache),
]
