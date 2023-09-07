from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest

@pytest.mark.django_db
class TestCategoryFullUpdate:

    def test_admin_full_update_category(self, api_client, create_category, admin_user):
        category = create_category(name='Test Category', description='This is a test category.')
        api_client.force_authenticate(user=admin_user)

        updated_data = {
            'name': 'Updated Test Category',
            'description': 'Updated description for the category.'
        }

        response = api_client.put(reverse('categories:category-retrive-update-delete', args=[category.id]), updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == updated_data['name']

    def test_non_admin_full_update_category(self, api_client, create_category, regular_user):
        category = create_category(name='Test Category', description='This is a test category.')
        api_client.force_authenticate(user=regular_user)

        updated_data = {
            'description': 'Updated description for the category.'
        }

        response = api_client.put(reverse('categories:category-retrive-update-delete', args=[category.id]), updated_data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
