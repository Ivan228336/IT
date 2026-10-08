from django.contrib.auth import get_user_model

User = get_user_model()


def check_email(email: str) -> bool:
    """Функция для проверки занят ли email."""
    if not User.objects.filter(email=email).exists():
        return True
    return False
