from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest


@pytest.mark.django_db
class TestOrderList:

    def test_authenticated_owner_user_can_list_orders(self, api_client, create_order, regular_user):
        api_client.force_authenticate(user=regular_user)
        order1 = create_order(user=regular_user)
        order2 = create_order(user=regular_user)

        response = api_client.get(reverse('orders:order-list-create'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_authenticated_user_can_list_only_his_orders(self, api_client, create_order, regular_user, another_user):
        api_client.force_authenticate(user=regular_user)
        """ order created by regular_user """
        order1 = create_order(user=regular_user)


        api_client.force_authenticate(user=another_user)        
        """  orders created by another_user """
        order2 = create_order(user=another_user)
        order3 = create_order(user=another_user)
        order4 = create_order(user=another_user)

        response = api_client.get(reverse('orders:order-list-create'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3  # Only the order created by another_user should be visible


    def test_anonymous_user_can_not_list_orders(self, api_client, regular_user, create_order):
        order = create_order(user=regular_user)

        response = api_client.get(reverse('orders:order-list-create'))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED




    
