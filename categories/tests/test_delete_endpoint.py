from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest

from categories.models import Category


@pytest.mark.django_db
class TestCategoryUpdate:
    
    def test_admin_delete_category(self, api_client, create_category, admin_user):
        category = create_category(name='Test Category', description='This is a test category.')
        api_client.force_authenticate(user=admin_user)
        

        response = api_client.delete(reverse('categories:category-retrive-update-delete', args=[category.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Category.objects.filter(id=category.id).exists()


    def test_non_admin_delete_category(self, api_client, create_category, regular_user):
        category = create_category(name='Test Category', description='This is a test category.')
        api_client.force_authenticate(user=regular_user)

        updated_data = {
            'description': 'Updated description for the category.'
        }

        response = api_client.delete(reverse('categories:category-retrive-update-delete', args=[category.id]))
        assert response.status_code == status.HTTP_403_FORBIDDEN

