from ninja import Schema


class EmailAvailable(Schema):
    message: str | None
    error: str | None
    available: bool
