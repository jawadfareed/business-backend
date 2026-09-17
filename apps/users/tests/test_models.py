import pytest
from apps.users.models import User


@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(email="test@example.com", password="Password123!")
    assert user.email == "test@example.com"
    assert user.check_password("Password123!")
    assert user.is_active is True
