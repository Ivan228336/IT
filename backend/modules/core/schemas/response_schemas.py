from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None


class SuccessResponse(BaseModel):
    success: bool
    message: str
    detail: str | None = None
