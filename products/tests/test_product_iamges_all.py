from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest
import os

from categories.models import Category
from products.models import Product, ProductImage
from products.utils import set_default_product_test_image

@pytest.mark.django_db
class TestProductImageCreateView:


    def test_authenticated_user_can_upload_single_image_for_product(self, create_category, create_product, api_client, regular_user):
        pass # wil implement soon!


    def test_unauthenticated_user_cannot_upload_single_image_for_product(self, create_category, create_product, api_client, regular_user):
        # Create a product
        category = create_category("Category 1", "Description 1")
        product = create_product(regular_user, "Product 1", "Description 1", category, 200.00)

        # Use api_client to send a POST request to the product's images endpoint with a single image file
        data = {'image': set_default_product_test_image()}
        response = api_client.post(reverse('products:product-image-list-create', args=[product.id]), data, format='multipart')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_can_upload_multiple_images_for_product(self, create_category, create_product, api_client, regular_user):
        pass # will implement soon


    def test_unauthenticated_user_cannot_upload_multiple_images_for_product(self, create_category, create_product, api_client, regular_user):
        # Create a product
        category = create_category("Category 1", "Description 1")
        product = create_product(regular_user, "Product 1", "Description 1", category, 200.00)

        # Use api_client to send a POST request to the product's images endpoint with multiple image files
        data = {'image': [set_default_product_test_image(), set_default_product_test_image()]}
        response = api_client.post(reverse('products:product-image-list-create', args=[product.id]), data, format='multipart')

        # Assert that the response status code is 401 Unauthorized
        assert response.status_code == status.HTTP_401_UNAUTHORIZED



@pytest.mark.django_db
class TestProductImageUpdateDestroyView:

    def test_owner_product_can_update_product_image(self, create_category, create_product, api_client, regular_user):
        pass

    def test_nonowner_product_cannot_update_product_image(self, create_category, create_product, api_client, regular_user, another_user):
        pass

