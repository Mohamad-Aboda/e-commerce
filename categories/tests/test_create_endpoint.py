from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest


@pytest.mark.django_db
class TestCategoryCreate:

    def test_admin_create_category(self, api_client, create_category, admin_user):
        category = {'name': 'Test Category', 'description': 'This is a test category.'}
        api_client.force_authenticate(user=admin_user)

        response = api_client.post(reverse('categories:category-list-create'), category, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_non_admin_create_category(self, api_client, create_category, regular_user):
        category = {'name': 'Test Category', 'description': 'This is a test category.'}
        api_client.force_authenticate(user=regular_user)

        updated_data = {
            'description': 'Updated description for the category.'
        }

        response = api_client.post(reverse('categories:category-list-create'), category, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN


