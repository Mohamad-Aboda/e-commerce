from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest

@pytest.mark.django_db
class TestOrderRetrieveDestroy:

    def test_authenticated_user_can_retrieve_own_order(self, api_client, create_order, regular_user):
        api_client.force_authenticate(user=regular_user)
        order = create_order(user=regular_user)

        # Retrieve the order
        response = api_client.get(reverse('orders:order-retrieve-destroy', args=[order.id]))
        assert response.status_code == status.HTTP_200_OK
        # Check if the response contains the order details
        assert 'order_id' in response.data
        assert 'order_date' in response.data
        assert 'user' in response.data
        assert response.data['user']['id'] == regular_user.id

    def test_authenticated_user_cannot_retrieve_other_user_order(self, api_client, create_order, regular_user, another_user):
        api_client.force_authenticate(user=regular_user)
        order = create_order(user=another_user)

        # Try to retrieve the other user's order
        response = api_client.get(reverse('orders:order-retrieve-destroy', args=[order.id]))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    


