import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from orders.models import Order, OrderItem
from products.models import Product


@pytest.mark.django_db
class TestOrderItemDelete:


    def test_authenticated_user_can_delete_items_in_own_order(self, api_client, create_category, create_order_item, create_order, create_product, regular_user, another_user):
        api_client.force_authenticate(user=regular_user)


        order = create_order(user=regular_user)
        category = create_category(name='Category 1', description='Description 1')
        product = create_product(user=regular_user, name='Product 1', 
                        description='Description 1', category=category, price=200.00)
        order_item = create_order_item(order, product, 2)

        response = api_client.delete(reverse('orders:order-item-retrieve-update-destroy', args=[order.id, order_item.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_authenticated_user_cannot_delete_items_in_other_user_order(self, api_client, create_category, create_order_item, create_order, create_product, regular_user, another_user):
        api_client.force_authenticate(user=regular_user)


        order = create_order(user=another_user)
        category = create_category(name='Category 1', description='Description 1')
        product = create_product(user=another_user, name='Product 1', 
                        description='Description 1', category=category, price=200.00)
        order_item = create_order_item(order, product, 2)

        response = api_client.delete(reverse('orders:order-item-retrieve-update-destroy', args=[order.id, order_item.id]))
        assert response.status_code == status.HTTP_404_NOT_FOUND


