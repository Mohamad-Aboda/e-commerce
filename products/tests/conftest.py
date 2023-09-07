from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
import pytest

from categories.models import Category
from products.models import Product

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

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

@pytest.fixture
def get_jwt_token():
    user = User.objects.create_user(email='test@example.com', password='testpassword')
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

@pytest.fixture
def admin_user():
    user = User.objects.create_user(email='admin@example.com', password='adminpassword', is_staff=True, is_superuser=True)
    return user

@pytest.fixture
def regular_user():
    user = User.objects.create_user(email='user@example.com', password='userpassword')
    return user

@pytest.fixture
def another_user():
    user = User.objects.create_user(email='anotheruser@example.com', password='userpassword')
    return user