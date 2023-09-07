
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest

from categories.models import Category
from products.models import Product

@pytest.mark.django_db
class TestFullCategoryUpdate:

    def test_product_owner_full_update_category(self, create_category, create_product, api_client, regular_user):
        # Create a category with the old name ('Category 1')
        old_category = create_category(name='Category 1', description='Description 1')
        new_category = create_category(name='Category 2', description='Description 2')
        product = create_product(user=regular_user, name='Product 1', 
                        description='Description 1',category=old_category, price=200.00)

        api_client.force_authenticate(user=regular_user)

        updated_data = {
            'name': 'Product Name Updated',  # Updated name
            'description': 'Updated description.',
            "price": 200.00,
            "category": "Category 2",  # Updated category name
        }
        response = api_client.put(reverse('products:product-retrieve-update-destroy', args=[product.id]), updated_data, format='json')

        assert response.status_code == status.HTTP_200_OK

        product.refresh_from_db()

        assert product.category.name == new_category.name
        assert product.name == "Product Name Updated"
        assert product.description == "Updated description."

    


    def test_product_non_owner_full_update_category(self, create_category, create_product, api_client, regular_user, another_user):
        # Create a category with the old name ('Category 1')
        old_category = create_category(name='Category 1', description='Description 1')
        new_category = create_category(name='Category 2', description='Description 2')
        product = create_product(user=regular_user, name='Product 1', 
                        description='Description 1', category=old_category, price=200.00)

        api_client.force_authenticate(user=another_user)

        updated_data = {
            'name': 'Product Name Updated',  # Updated name
            'description': 'Updated description.',
            "price": 200.00,
            "category": "Category 2",  # Updated category name
        }
        response = api_client.put(reverse('products:product-retrieve-update-destroy', args=[product.id]), updated_data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

        product.refresh_from_db()

        assert product.category.name == old_category.name
