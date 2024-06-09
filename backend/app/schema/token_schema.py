from pydantic import (
    BaseModel,
    Field,
)


class TokenCreate(BaseModel):
    user_id: int
    token: str
    status: bool | None = Field(default=True)

    class config:
        orm_mode: True


class TokenUpdate(BaseModel):
    status: bool
