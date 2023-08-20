import json
from rest_framework.test import APIClient
from rest_framework import status
import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_data():
    return {
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'testpassword',
    }

@pytest.mark.django_db
def test_create_user(api_client, user_data):
    response = api_client.post(reverse('accounts:create-user'), user_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_retrieve_user(api_client, user_data):
    user = User.objects.create_user(**user_data)
    api_client.force_authenticate(user=user)

    response = api_client.get(reverse('accounts:update-user'))
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_update_user(api_client, user_data):
    user = User.objects.create_user(**user_data)
    api_client.force_authenticate(user=user)

    updated_data = {
        'first_name': 'Updated First Name',
        'last_name': 'Updated Last Name',
        'email':'test2@example.com',
        'password': 'updatepassword'
    }

    response = api_client.put(reverse('accounts:update-user'), updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == updated_data['first_name']
    assert response.data['last_name'] == updated_data['last_name']

@pytest.mark.django_db
def test_partial_update_user(api_client, user_data):
    user = User.objects.create_user(**user_data)
    api_client.force_authenticate(user=user)

    updated_data = {
        'first_name': 'Updated First Name',
    }

    response = api_client.patch(reverse('accounts:update-user'), updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == updated_data['first_name']
    assert response.data['last_name'] == user_data['last_name']
