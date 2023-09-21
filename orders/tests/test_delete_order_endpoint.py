from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest

@pytest.mark.django_db
class TestOrderDelete:

    def test_authenticated_user_can_delete_own_order(self, api_client, create_order, regular_user):
        api_client.force_authenticate(user=regular_user)
        order = create_order(user=regular_user)

        # Delete the order
        response = api_client.delete(reverse('orders:order-retrieve-destroy', args=[order.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_authenticated_user_cannot_delete_other_user_order(self, api_client, create_order, regular_user, another_user):
        api_client.force_authenticate(user=regular_user)
        order = create_order(user=another_user)

        # Try to delete the other user's order
        response = api_client.delete(reverse('orders:order-retrieve-destroy', args=[order.id]))
        assert response.status_code == status.HTTP_404_NOT_FOUND


    def test_anonymous_user_cannot_delete_order(self, api_client, create_order, regular_user):
        order = create_order(user=regular_user)
        # Try to delete an order without authentication
        response = api_client.delete(reverse('orders:order-retrieve-destroy', args=[order.id]))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
