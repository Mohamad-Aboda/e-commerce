from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest

from products.models import Product

@pytest.mark.django_db
class TestProductCreate:

    def test_authenticated_user_create_product(self, create_category, api_client, regular_user):
        
        category = create_category(name='Category 1', description='Description 1')
        api_client.force_authenticate(user=regular_user)

        response = api_client.post(reverse('products:product-list-create'), {
            "name": "Product 1",
            "description": "Description 1",
            "price": 200,
            "category": category.name,
            "user":regular_user
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.count() == 1

        product = Product.objects.first()
        assert product.name == 'Product 1'
        assert product.description == 'Description 1'
        assert product.category == category
        assert product.user == regular_user

        

    def test_unauthenticated_user_can_not_create_product(self, create_category, api_client):
        category = create_category(name='Category 1', description='Description 1')
        
        response = api_client.post(reverse('products:product-list-create'), {
            "name": "Product 1",
            "description": "Description 1",
            "price": 200,
            "category": category.name
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Product.objects.count() == 0
