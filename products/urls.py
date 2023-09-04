from django.urls import path

from .apis import (ProductRetrieveUpdateDestroyView, ProductListCreateView,
                    ProductImageListCreateView, ProductImageRetrieveUpdateDestroyView,
                    ProductImagesDeleteSingleImageView, ProductImagesDeleteAllImagesView)

app_name = 'products'
urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-retrieve-update-destroy'),

    path('products/<int:product_id>/images/', ProductImageListCreateView.as_view(), name='product-image-list-create'),
    path('products/<int:product_id>/images/<int:image_id>/', ProductImageRetrieveUpdateDestroyView.as_view(), name='product-image-retrieve-update-destroy'),
    path('products/<int:product_id>/images/delete-all/', ProductImagesDeleteAllImagesView.as_view(), name='product-image-delete-all-images'),



]