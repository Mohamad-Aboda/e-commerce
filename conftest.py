from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import pytest

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()


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