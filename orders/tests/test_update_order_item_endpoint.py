import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from orders.models import Order, OrderItem
from products.models import Product


@pytest.mark.django_db
class TestOrderItemUpdate:

    def test_authenticated_user_can_update_items_in_own_order(self, create_category, api_client, 
    create_order, create_product, create_order_item, regular_user):

        api_client.force_authenticate(regular_user)

        order = create_order(user=regular_user)
        category = create_category(name='Category 1', description='Description 1')
        product = create_product(user=regular_user, name='Product 1', 
                        description='Description 1', category=category, price=200.00)
        order_item = create_order_item(order, product, 2)

        updated_data = {
            "quantity": 4
        }

        response = api_client.put(reverse('orders:order-item-retrieve-update-destroy', args=[order.id, order_item.id]), data=updated_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['quantity'] == 4

    def test_authenticated_user_cannot_update_items_in_other_user_order(self, create_category,another_user, api_client, 
    create_order, create_product, create_order_item, regular_user):
        
        api_client.force_authenticate(user=regular_user)

        order = create_order(user=another_user)
        category = create_category(name='Category 1', description='Description 1')
        product = create_product(user=another_user, name='Product 1', 
                        description='Description 1', category=category, price=200.00)
        order_item = create_order_item(order, product, 2)

        updated_data = {
            "quantity": 44
        }

        response = api_client.put(reverse('orders:order-item-retrieve-update-destroy', args=[order.id, order_item.id]), data=updated_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

