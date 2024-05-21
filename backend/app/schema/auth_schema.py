from typing import Optional

from fastapi import Form
from pydantic import BaseModel, EmailStr, Field, computed_field
from typing_extensions import Annotated

from app.schema.base_schema import ModelBaseInfo
from app.services.image_service import image_service


class BaseUser(BaseModel):
    role_id: int | None = Field(default=None)
    full_name: str
    email: EmailStr
    avatar: str | None = Field(default=None)

    class config:
        orm_mode: True


class CreateUserRequest(BaseUser):
    full_name: str = Form(...)
    email: EmailStr = Form(...)
    password: str = Form(..., min_length=6)
    avatar: str = Form(None)


class ProfileUpdateRequest(BaseModel):
    full_name: str | None = Field(default=None)
    username: EmailStr | None = Field(default=None)


class User(ModelBaseInfo, BaseUser):
    pass


class CreateUserResponse(BaseUser):
    id: int

    @computed_field
    @property
    def avatar_url(self) -> Optional[str]:
        if self.avatar:
            return image_service.get_file(self.avatar)
        return None

    @property
    def test(self) -> Optional[str]:
        if self.avatar:
            return image_service.get_file(self.avatar)
        return None

    class config:
        fields = {"avatar": "_test"}
