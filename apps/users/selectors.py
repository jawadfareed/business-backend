from typing import Optional
from django.db.models import QuerySet
from apps.users.models import User


def user_get_by_id(user_id: int) -> Optional[User]:
    """
    Fetch an active user by primary key ID.
    """
    try:
        return User.objects.get(id=user_id, is_active=True)
    except User.DoesNotExist:
        return None


def user_get_by_email(email: str) -> Optional[User]:
    """
    Fetch an active user by email address.
    """
    try:
        return User.objects.get(email__iexact=email, is_active=True)
    except User.DoesNotExist:
        return None


def user_list_active() -> QuerySet[User]:
    """
    Return all active users queryset.
    """
    return User.objects.filter(is_active=True)
