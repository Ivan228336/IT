from pydantic import BaseModel


class LogoutInputDTO(BaseModel):
    access_token: str
    refresh_token: str
