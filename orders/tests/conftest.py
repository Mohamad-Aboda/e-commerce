
import pytest
from orders.models import Order, OrderItem
from categories.models import Category
from products.models import Product

@pytest.fixture
def create_order():
    def _create_order(user):
        return Order.objects.create(user=user)
    return _create_order

@pytest.fixture
def create_order_item(create_order, create_product):
    def _create_order_item(order, product, quantity):
        return OrderItem.objects.create(order=order, product=product, quantity=quantity)
    return _create_order_item


@pytest.fixture
def create_product():
    def _create_product(user, name, description, category, price):
        return Product.objects.create(user=user, name=name, description=description, category=category, price=price)
    return _create_product


@pytest.fixture
def create_category():
    def _create_category(name, description):
        return Category.objects.create(name=name, description=description)
    return _create_category



