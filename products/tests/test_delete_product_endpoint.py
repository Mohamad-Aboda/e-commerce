from django.urls import reverse
from rest_framework import status
import pytest

@pytest.mark.django_db
class TestProductDelete:

    def test_product_owner_delete_product(self, create_category, create_product, api_client, regular_user):
        # Create a category
        category = create_category(name='Category 1', description='Description 1')
        product = create_product(user=regular_user, name='Product 1', 
                        description='Description 1', category=category, price=200.00)
        api_client.force_authenticate(user=regular_user)
        response = api_client.delete(reverse('products:product-retrieve-update-destroy', args=[product.id]))

        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = api_client.get(reverse('products:product-retrieve-update-destroy', args=[product.id]))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_product_non_owner_delete_product(self, create_category, create_product, api_client, regular_user, another_user):
        # Create a category
        category = create_category(name='Category 1', description='Description 1')
        product = create_product(user=another_user, name='Product 1', 
                        description='Description 1', category=category, price=200.00)

        api_client.force_authenticate(user=regular_user)
        response = api_client.delete(reverse('products:product-retrieve-update-destroy', args=[product.id]))

        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Attempt to retrieve the product (should still exist)
        response = api_client.get(reverse('products:product-retrieve-update-destroy', args=[product.id]))
        assert response.status_code == status.HTTP_200_OK
