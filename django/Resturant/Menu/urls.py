from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.MenuListCreateView.as_view(), name='menu-list-create'),
    path('<int:menu_id>/', views.MenuDetailView.as_view(), name='menu-detail'),
]
