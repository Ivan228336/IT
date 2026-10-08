from django.contrib.auth import get_user_model

User = get_user_model()


class PasswordRecoveryResponseRepository:
    @staticmethod
    def user_exists(email: str) -> bool:
        if User.objects.filter(email=email).exists():
            return True
        return False

    @staticmethod
    def get_user_by_email(email: str) -> User | None:
        return User.objects.get(email=email)

    @staticmethod
    def set_user_password(user: User, new_password: str) -> None:
        user.set_password(new_password)
        user.save()
