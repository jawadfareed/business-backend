import pytest
from apps.users.services import user_create, user_update


@pytest.mark.django_db
def test_user_create_service():
    user = user_create(email="service@example.com", password="Password123!", first_name="John")
    assert user.email == "service@example.com"
    assert user.first_name == "John"


@pytest.mark.django_db
def test_user_update_service():
    user = user_create(email="update@example.com", password="Password123!")
    updated_user = user_update(user=user, first_name="Jane", last_name="Doe")
    assert updated_user.first_name == "Jane"
    assert updated_user.last_name == "Doe"
