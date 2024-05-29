from typing import Optional

from email_validator import validate_email
from fastapi import HTTPException, status
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ValidationError,
    computed_field,
    field_validator,
)

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
    full_name: str
    email: EmailStr
    password: str = Field(..., min_length=6)
    avatar: str | None = Field(default=None)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        try:
            validate_email(value, check_deliverability=False)
        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid email",
            )
        return value


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


class FullUserResponse(CreateUserResponse):
    is_active: bool
    is_email_verified: bool


class LoginResponse(BaseModel):
    msg: str
    user: dict


class UserProfileResponse(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
