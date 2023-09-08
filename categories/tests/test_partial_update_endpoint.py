from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest

@pytest.mark.django_db
class TestCategoryPartialUpdate:
    
    def test_admin_partial_update_category(self, api_client, create_category, admin_user):
        category = create_category(name='Test Category', description='This is a test category.')
        api_client.force_authenticate(user=admin_user)
        
        updated_data = {
            'description': 'Updated description for the category.'
        }

        response = api_client.patch(reverse('categories:category-retrive-update-delete', args=[category.id]), updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['description'] == updated_data['description']

    def test_non_admin_partial_update_category(self, api_client, create_category, regular_user):
        category = create_category(name='Test Category', description='This is a test category.')
        api_client.force_authenticate(user=regular_user)

        updated_data = {
            'description': 'Updated description for the category.'
        }

        response = api_client.patch(reverse('categories:category-retrive-update-delete', args=[category.id]), updated_data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
