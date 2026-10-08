from pydantic import BaseModel


class UpdateTokenInputDTO(BaseModel):
    refresh: str
