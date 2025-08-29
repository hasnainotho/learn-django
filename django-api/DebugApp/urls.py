from django.urls import path, include
from . import views

urlpatterns = [
    path('numbers/', views.display_even_numbers, name='display_even_numbers'),
]