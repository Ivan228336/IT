from django.contrib.auth import get_user_model

User = get_user_model()


class CheckVerifyRepository:
    @staticmethod
    def make_user_active(user_id: int) -> User:
        user = User.custom_object_auth_manager.get(id=user_id)
        user.is_active = True
        user.save()
        return user
