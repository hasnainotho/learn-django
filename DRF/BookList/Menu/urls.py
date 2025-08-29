from django.urls import path
from . import views


urlpatterns = [
    path('', views.MenuView.as_view()),
    path('<int:pk>', views.Menu.as_view())
]
