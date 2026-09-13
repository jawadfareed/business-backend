from typing import Optional
from django.db import transaction
from apps.users.models import User


@transaction.atomic
def user_create(
    *,
    email: str,
    password: str,
    first_name: str = "",
    last_name: str = "",
    phone_number: str = "",
    is_active: bool = True,
    is_staff: bool = False
) -> User:
    """
    Service function for user creation.
    Encapsulates creation business logic and database transaction.
    """
    user = User(
        email=email,
        username=email,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        is_active=is_active,
        is_staff=is_staff,
    )
    user.set_password(password)
    user.full_clean()
    user.save()
    return user


@transaction.atomic
def user_update(
    *,
    user: User,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    phone_number: Optional[str] = None
) -> User:
    """
    Service function for updating user profile fields.
    """
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if phone_number is not None:
        user.phone_number = phone_number

    user.full_clean()
    user.save()
    return user
