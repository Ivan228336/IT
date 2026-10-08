from pydantic import BaseModel


class PasswordRecoveryInputDTO(BaseModel):
    email: str
