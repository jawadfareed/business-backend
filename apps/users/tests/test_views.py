import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_user_api():
    client = APIClient()
    url = reverse('users_v1:list-create')
    data = {
        "email": "apiuser@example.com",
        "password": "Password123!",
        "first_name": "API",
        "last_name": "User"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data["email"] == "apiuser@example.com"
