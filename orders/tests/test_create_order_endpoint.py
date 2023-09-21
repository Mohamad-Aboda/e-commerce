from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest

@pytest.mark.django_db
class TestOrderCreate:

    def test_authenticated_user_can_create_orders(self, api_client, regular_user, create_order):
        api_client.force_authenticate(user=regular_user)

        # Create a new order
        response = api_client.post(reverse('orders:order-list-create'))
        assert response.status_code == status.HTTP_201_CREATED

        # Check if the response contains the order details
        assert 'order_details' in response.data
        assert 'msg' in response.data
        assert response.data['msg'] == 'Order created successfully'
        assert 'order_id' in response.data['order_details']
        assert 'order_date' in response.data['order_details']
        assert 'user' in response.data['order_details']
        assert 'total_price' in response.data['order_details']
        assert response.data['order_details']['user']['id'] == regular_user.id

    def test_anonymous_user_can_not_create_orders(self, api_client, regular_user, create_order):
        # Attempt to create an order without authentication
        order = create_order(user=regular_user)
        response = api_client.post(reverse('orders:order-list-create'))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
