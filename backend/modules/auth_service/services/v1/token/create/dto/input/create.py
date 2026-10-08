from django.contrib.auth import get_user_model
from pydantic import BaseModel

User = get_user_model()


class AuthInputDTO(BaseModel):
    user_id: int
