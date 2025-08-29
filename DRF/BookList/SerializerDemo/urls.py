from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_all),
    path('<int:pk>/', views.get_item),
    path('create-item/', views.create_item),
]