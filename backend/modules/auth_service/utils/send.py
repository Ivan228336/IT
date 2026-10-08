from datetime import UTC, datetime, timedelta

import jwt
from django.contrib.auth import get_user_model
from django.utils.html import escape

from config.settings import settings
from modules.auth_service.tasks import send_email_task

User = get_user_model()


class SendEmailTask:
    @staticmethod
    def verify_by_email(user: User) -> None:
        """Генерация и отправка токена подтверждения email."""
        payload = {
            "user_id": str(user.id),
            "email": user.email,
            "exp": int((datetime.now(UTC) + timedelta(days=1)).timestamp()),
            "iat": int((datetime.now(UTC)).timestamp()),
        }

        verification_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        frontend_url = settings.FRONTEND_URL

        verify_url = f"{frontend_url}/verify?token={verification_token}"

        send_email_task.delay(
            subject="Подтвердите ваш email",
            message=f"""
                Здравствуйте, {escape(user.username)}!

                Для подтверждения email перейдите по ссылке:
                {verify_url}

                Ссылка действительна 24 часа.

                Если вы не регистрировались, проигнорируйте это письмо.
                """,
            email_address=user.email,
        )

    @staticmethod
    def async_send(email: str, new_pass: str) -> None:
        """Функция для отправки письма при потере пароля."""
        send_email_task.delay(
            "Измените пароль",
            f"""
                                    Здравствуйте!
                                    По вашему запросу был сгенерирован новый пароль для входа в Систему “Гуляем”.
                                    Ваш новый пароль: {new_pass}
                                    Обратите внимание:
                                    1.  Используйте этот пароль для входа в систему. Данный пароль является бессрочным,
                                     вы можете использовать его для дальнейшей авторизации в системе. 
                                    2.  Сразу после входа настоятельно рекомендуем сменить пароль в личном кабинете в
                                     разделе «Мой профиль».
                                    3. Не передавайте пароль третьим лицам.
                                    4.  Если вы не запрашивали восстановление пароля, проигнорируйте это письмо или 
                                    обратитесь в службу поддержки.
                                    ---
                                    С уважением,
                                    Команда “Гуляем”
                                    """,
            email,
        )
