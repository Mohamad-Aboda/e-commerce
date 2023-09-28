import pytest
from orders.models import Order, OrderItem
from products.models import Product
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestOrderItemList:

    def test_authenticated_owner_user_can_list_order_items(self, api_client, create_category, create_order, create_product, regular_user, create_order_item):
        api_client.force_authenticate(user=regular_user)

        """ Create Product """
        category = create_category(name='Category 1', description='Description 1')
        product = create_product(user=regular_user, name='Product 1', 
                        description='Description 1', category=category, price=200.00)
        """ Create Order """
        order = create_order(user=regular_user)
        """ Add Item to the order """
        order_item = create_order_item(order, product, 2)

        response = api_client.get(reverse('orders:order-item-list-create', args=[order.id]))
        assert response.status_code == status.HTTP_200_OK

        # Check if the response contains the order item details
        assert len(response.data) == 1
        assert response.data[0]['product']['id'] == product.id
        assert response.data[0]['quantity'] == 2

    def test_authenticated_user_can_list_only_his_order_items(self, api_client, create_category, create_order, create_product, regular_user, another_user, create_order_item):
        api_client.force_authenticate(user=regular_user)

        """ Create Product """
        category1 = create_category(name='Category 1', description='Description 1')
        product1 = create_product(user=regular_user, name='Product 1', 
                        description='Description 1', category=category1, price=200.00)
        """ Create Order """
        order1 = create_order(user=regular_user)
        """ Add Item to the order """
        order_item1 = create_order_item(order1, product1, 1)

        """ Create another order for another user """
        api_client.force_authenticate(user=another_user)

        """ Create Product """
        category2 = create_category(name='Category 2', description='Description 2')
        product2 = create_product(user=another_user, name='Product 1', 
                        description='Description 1', category=category2, price=200.00)
        """ Create Order """
        order2 = create_order(user=another_user)
        """ Add Item to the order """
        order_item2 = create_order_item(order2, product2, 2)

        response = api_client.get(reverse('orders:order-item-list-create', args=[order2.id]))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['product']['id'] == product2.id
        assert response.data[0]['quantity'] == 2

    def test_anonymous_user_can_not_list_order_items(self, api_client, create_category, create_order, create_product, regular_user, create_order_item):
        # Create a new order
        """ Create Product """
        category1 = create_category(name='Category 1', description='Description 1')
        product1 = create_product(user=regular_user, name='Product 1', 
                        description='Description 1', category=category1, price=200.00)
        """ Create Order """
        order1 = create_order(user=regular_user)
        """ Add Item to the order """
        order_item1 = create_order_item(order1, product1, 1)

        # Attempt to retrieve order items without authentication
        orderResponse = api_client.get(reverse('orders:order-list-create'))
        if orderResponse.status_code == status.HTTP_200_OK:
            itemResponse = api_client.get(reverse('orders:order-item-list-create', args=[order1.id]))
            assert itemResponse.status_code == status.HTTP_401_UNAUTHORIZED
        else:
            assert orderResponse.status_code == status.HTTP_401_UNAUTHORIZED


