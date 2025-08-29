from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('<int:order_id>/', views.OrderDetailView.as_view(), name='order-detail'),
]


# urlpatterns = [
#     path('create/', create_order, name='create_order'),
#     path('get/<int:order_id>/', get_order, name='get_order'),
#     path('list/', list_orders, name='list_orders'),
#     path('delete/<int:order_id>/', delete_order, name='delete_order'),
#     path('update/<int:order_id>/', update_order, name='update_order'),
# ]