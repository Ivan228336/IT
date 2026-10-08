from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterUserRepository:
    @staticmethod
    def check_email(email: str) -> bool:
        if User.custom_object_auth_manager.filter(email=email).exists():
            return True
        return False

    @staticmethod
    def check_username(username: str) -> bool:
        if User.custom_object_auth_manager.filter(username=username).exists():
            return True
        return False

    @staticmethod
    def create_user(username: str, email: str, password: str) -> User:
        user = User.custom_object_auth_manager.create_user(
            username=username, email=email, password=password, is_active=False
        )
        return user
