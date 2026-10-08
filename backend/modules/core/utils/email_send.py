from modules.auth_service.tasks import send_email_task
from ninja import Router

email_check_router = Router()



def email_async_test(email, username):
    send_email_task.delay('Тест', f'Привет {username}', email)


@email_check_router.get("test_send/{message}/{to}")
def test_sender(request, message: str, to: str):
    email_async_test(email=to, username=message)
    return {"message": message,
            "to": to,
            "send": "Yes"}