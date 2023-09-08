from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest

from categories.models import Category
from products.models import Product, ProductImage
from products.utils import set_default_product_test_image

@pytest.mark.django_db
class TestProductImageDelete:

    def test_owner_delete_product_single_image(self, create_category, create_product, api_client, regular_user):
        # Create a product with a single image
        category = create_category("Category 1", "Description 1")
        product = create_product(regular_user, "Product 1", "Description 1", category, 200.00)
        image = ProductImage.objects.create(product=product, image=set_default_product_test_image())  # Replace 'your_image_file' with the actual image file.

        api_client.force_authenticate(user=regular_user)

        # Delete the image using the endpoint
        response = api_client.delete(reverse('products:product-image-retrieve-update-destroy', args=[product.id, image.id]))

        # Assert the response status code and the image count for the product
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert ProductImage.objects.filter(product=product).count() == 0

    def test_owner_delete_product_multiple_images(self, create_category, create_product, api_client, regular_user):
        # Create a product with multiple images
        category = create_category("Category 1", "Description 1")
        product = create_product(regular_user, "Product 1", "Description 1", category, 200.00)
        image1 = ProductImage.objects.create(product=product, image=set_default_product_test_image())  # Replace 'your_image_file1' with the actual image file.
        image2 = ProductImage.objects.create(product=product, image=set_default_product_test_image())  # Replace 'your_image_file2' with the actual image file.

        api_client.force_authenticate(user=regular_user)

        # Delete one of the images using the endpoint
        response = api_client.delete(reverse('products:product-image-delete-all-images', args=[product.id]))

        # Assert the response status code and the image count for the product
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert ProductImage.objects.filter(product=product).count() == 0

    def test_non_owner_delete_product_single_image(self, create_category, create_product, api_client, regular_user, another_user):
        # Create a product with a single image by the admin user
        category = create_category("Category 1", "Description 1")
        product = create_product(regular_user, "Product 1", "Description 1", category, 200.00)
        image = ProductImage.objects.create(product=product, image=set_default_product_test_image())  # Replace 'your_image_file' with the actual image file.

        api_client.force_authenticate(user=another_user)

        # Attempt to delete the image using the endpoint
        response = api_client.delete(reverse('products:product-image-retrieve-update-destroy', args=[product.id, image.id]))

        # Assert the response status code and the image count for the product (should not change)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert ProductImage.objects.filter(product=product).count() == 1

    def test_non_owner_delete_product_multiple_images(self, create_category, create_product, api_client, regular_user, another_user):
        # Create a product with multiple images by the admin user
        category = create_category("Category 1", "Description 1")
        product = create_product(regular_user, "Product 1", "Description 1", category, 200.00)
        image1 = ProductImage.objects.create(product=product, image=set_default_product_test_image())  # Replace 'your_image_file1' with the actual image file.
        image2 = ProductImage.objects.create(product=product, image=set_default_product_test_image())  # Replace 'your_image_file2' with the actual image file.

        api_client.force_authenticate(user=another_user)

        # Attempt to delete one of the images using the endpoint
        response = api_client.delete(reverse('products:product-image-delete-all-images', args=[product.id]))

        # Assert the response status code and the image count for the product (should not change)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert ProductImage.objects.filter(product=product).count() == 2
