from django.shortcuts import render
from django.urls import path, include
from . import views

urlpatterns = [
    path('throttle-test/', views.throttle_view),
    path('user-throttle/', views.user_throttle),
    path('ten-throttle/', views.ten_throttle),
    path('secret/', views.secret),
    path('manager/', views.manager_view),
    path('view/', views.TestViewSet.as_view()),
    path('view/<int:pk>', views.TestDetailViewSet.as_view()),
]