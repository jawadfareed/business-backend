from celery import shared_task
from apps.users.selectors import user_get_by_id


@shared_task
def send_welcome_email(user_id: int):
    """
    Sample asynchronous Celery task for user onboarding.
    """
    user = user_get_by_id(user_id)
    if user:
        # Task logic (e.g. sending email)
        print(f"Sending welcome email to {user.email}")
        return True
    return False
