from datetime import datetime

from pydantic import BaseModel


class AuthOutputDTOSuccess(BaseModel):
    success: bool
    access: str
    refresh: str
    access_exp: str
    refresh_exp: str

    @classmethod
    def from_result(cls, result: dict) -> "AuthOutputDTOSuccess":
        return cls(
            success=result["success"],
            access=result["access"],
            refresh=result["refresh"],
            access_exp=datetime.fromtimestamp(result["access_exp"]).isoformat(),
            refresh_exp=datetime.fromtimestamp(result["refresh_exp"]).isoformat(),
        )


class AuthOutputDTOError(BaseModel):
    error: str
    detail: str

    @classmethod
    def from_result(cls, result: dict) -> "AuthOutputDTOError":
        return cls(error=result["error"], detail=result["detail"])


AuthOutputDTO = AuthOutputDTOSuccess | AuthOutputDTOError
