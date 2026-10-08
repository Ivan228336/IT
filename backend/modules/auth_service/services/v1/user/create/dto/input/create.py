from pydantic import BaseModel


class RegisterUserInputDTO(BaseModel):
    username: str
    email: str
    password: str
