from django.urls import path
from .apis import (OrderListCreateView, OrderRetrieveDestroyView,
                    OrderItemListCreateView, OrderItemRetrieveUpdateDestroyView)

app_name = 'orders'

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:order_pk>/', OrderRetrieveDestroyView.as_view(), name='order-retrieve-destroy'),

    path('orders/<int:order_pk>/items/', OrderItemListCreateView.as_view(), name='order-item-list-create'),
    path('orders/<int:order_pk>/items/<int:item_pk>/', OrderItemRetrieveUpdateDestroyView.as_view(), name='order-item-retrieve-update-destroy'),
]
