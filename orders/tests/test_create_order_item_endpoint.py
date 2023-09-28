import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from orders.models import Order, OrderItem
from products.models import Product


@pytest.mark.django_db
class TestOrderItemCreate:

    def test_authenticated_user_can_add_items_its_own_order(self, create_category, api_client, create_order, create_product, regular_user):
        api_client.force_authenticate(user=regular_user)

        order = create_order(user=regular_user)
        category = create_category(name='Category 1', description='Description 1')
        product = create_product(user=regular_user, name='Product 1', 
                        description='Description 1', category=category, price=200.00)
       
        data = {
            "product": product.id,
            "quantity": 3
        }

        response = api_client.post(reverse('orders:order-item-list-create', args=[order.id]), data=data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_authenticated_user_cannot_add_items_to_other_user_order(self, create_category, api_client, create_order, create_product, regular_user, another_user):
        api_client.force_authenticate(user=regular_user)

        order = create_order(user=another_user)
        category = create_category(name='Category 1', description='Description 1')
        product = create_product(user=regular_user, name='Product 1', 
                        description='Description 1', category=category, price=200.00)

        data = {
            "product": product.id,
            "quantity": 3
        }

        response = api_client.post(reverse('orders:order-item-list-create', args=[order.id]), data=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

