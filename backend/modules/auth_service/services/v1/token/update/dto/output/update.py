from datetime import datetime

from pydantic import BaseModel


class UpdateTokenOutputDTOSuccess(BaseModel):
    success: bool
    access: str
    refresh: str
    access_exp: str
    refresh_exp: str

    @classmethod
    def from_result(cls, result: dict) -> "UpdateTokenOutputDTOSuccess":
        return cls(
            success=result["success"],
            access=result["access"],
            refresh=result["refresh"],
            access_exp=datetime.fromtimestamp(result["access_exp"]).isoformat(),
            refresh_exp=datetime.fromtimestamp(result["refresh_exp"]).isoformat(),
        )


class UpdateTokenOutputDTOError(BaseModel):
    error: str
    detail: str

    @classmethod
    def from_result(cls, result: dict) -> "UpdateTokenOutputDTOError":
        return cls(error=result["error"], detail=result["detail"])


UpdateTokenOutputDTO = UpdateTokenOutputDTOSuccess | UpdateTokenOutputDTOError
