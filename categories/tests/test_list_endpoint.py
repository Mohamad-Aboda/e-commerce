from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest


@pytest.mark.django_db
class TestCategoryList:

    def test_get_categories(self, create_category, api_client):
        create_category(name='Category 1', description='Description 1')
        create_category(name='Category 2', description='Description 2')

        response = api_client.get(reverse('categories:category-list-create'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_get_category_detail(self, create_category, api_client):
        category = create_category(name='Test Category', description='This is a test category.')

        response = api_client.get(reverse('categories:category-retrive-update-delete', args=[category.id]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == category.name

