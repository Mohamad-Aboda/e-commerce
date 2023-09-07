from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest


@pytest.mark.django_db
class TestListDetail:

    def test_get_products(self, create_category, create_product, api_client, regular_user):
        category = create_category(name='Category 1', description='Description 1')
        create_product(user=regular_user, name='Product 1', 
                        description='Description 1',category=category, price=200)

        response = api_client.get(reverse('products:product-list-create'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        
    
    def test_get_product_detail(self, create_category, create_product, api_client, regular_user):
        category = create_category(name='Test Category', description='This is a test category.')
        product = create_product(user=regular_user, name='Product 1', 
                        description='Description 1',category=category, price=200)

        response = api_client.get(reverse('products:product-retrieve-update-destroy', args=[product.id]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == product.name
        assert response.data['description'] == product.description

