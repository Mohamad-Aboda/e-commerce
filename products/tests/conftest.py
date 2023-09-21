import pytest

from categories.models import Category
from products.models import Product

@pytest.fixture
def create_category():
    def _create_category(name, description):
        return Category.objects.create(name=name, description=description)
    return _create_category

@pytest.fixture
def create_product():
    def _create_product(user, name, description, category, price):
        return Product.objects.create(user=user, name=name, description=description, category=category, price=price)
    return _create_product

