from django.db import models
from django.contrib.auth import get_user_model

from categories.models import Category
from .utils import product_image_directory_path





User = get_user_model()

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_directory_path, null=True, blank=True)

    def __str__(self):
        return self.product.name
    