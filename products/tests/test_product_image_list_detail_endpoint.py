from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest
import os

from categories.models import Category
from products.models import Product, ProductImage
from products.utils import set_default_product_test_image


@pytest.mark.django_db
class TestProductImageList:
    def test_anonymous_user_can_list_all_images_for_product(self, create_category, create_product, api_client, regular_user):
        # Create a product with some images
        category = create_category("Category 1", "Description 1")
        product = create_product(regular_user, "Product 1", "Description 1", category, 200.00)
        image1 = ProductImage.objects.create(product=product, image=set_default_product_test_image())
        image2 = ProductImage.objects.create(product=product, image=set_default_product_test_image())

        response = api_client.get(reverse('products:product-image-list-create', args=[product.id]))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # Assuming two images were created

    def test_authenticated_user_can_list_all_images_for_product(self, create_category, create_product, api_client, regular_user):
        category = create_category("Category 1", "Description 1")
        product = create_product(regular_user, "Product 1", "Description 1", category, 200.00)
        image1 = ProductImage.objects.create(product=product, image=set_default_product_test_image())
        image2 = ProductImage.objects.create(product=product, image=set_default_product_test_image())

        api_client.force_authenticate(user=regular_user)
        response = api_client.get(reverse('products:product-image-list-create', args=[product.id]))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # Assuming two images were created


@pytest.mark.django_db
class TestProductImageDetail:

    def test_anonymous_user_can_retrieve_product_image(self, create_category, create_product, api_client, regular_user):
        # Create a product with an image
        category = create_category("Category 1", "Description 1")
        product = create_product(regular_user, "Product 1", "Description 1", category, 200.00)
        image = ProductImage.objects.create(product=product, image=set_default_product_test_image())

        # Use api_client to send a GET request to retrieve the product's image
        response = api_client.get(reverse('products:product-image-retrieve-update-destroy', args=[product.id, image.id]))

        # Assert that the response status code is 200 OK
        assert response.status_code == status.HTTP_200_OK

        # Assert that the retrieved image data matches the created image
        assert response.data['id'] == image.id

    def test_authenticated_user_can_retrieve_product_image(self, create_category, create_product, api_client, regular_user):
        # Create a product with an image
        category = create_category("Category 1", "Description 1")
        product = create_product(regular_user, "Product 1", "Description 1", category, 200.00)
        image = ProductImage.objects.create(product=product, image=set_default_product_test_image())

        # Authenticate as regular_user
        api_client.force_authenticate(user=regular_user)

        # Use api_client to send a GET request to retrieve the product's image
        response = api_client.get(reverse('products:product-image-retrieve-update-destroy', args=[product.id, image.id]))

        # Assert that the response status code is 200 OK
        assert response.status_code == status.HTTP_200_OK

        # Assert that the retrieved image data matches the created image
        assert response.data['id'] == image.id