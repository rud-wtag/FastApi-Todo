from typing import Annotated, Optional

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.constants import (
    ADMIN,
    EMIL_NOT_VERIFIED_MESSAGE,
    UNAUTHORIZE_MESSAGE,
    USER,
)
from app.interface.jwt_token_interface import JWTTokenInterface
from app.services.jwt_token_service import JWTTokenService

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/v1/login")


def get_current_user(
    access_token: Annotated[Optional[str], Cookie()] = None,
    jwt_token_service: JWTTokenInterface = Depends(JWTTokenService),
) -> dict:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=UNAUTHORIZE_MESSAGE
        )
    user = jwt_token_service.verify_token(access_token)

    return user


def admin(user: dict = Depends(get_current_user)) -> dict:
    if user["role"] == ADMIN:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=UNAUTHORIZE_MESSAGE,
    )


def auth(user: dict = Depends(get_current_user)) -> dict:
    if user["role"] in {ADMIN, USER}:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=UNAUTHORIZE_MESSAGE,
    )


def active_user(user: dict = Depends(get_current_user)) -> dict:
    if user["is_active"]:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=UNAUTHORIZE_MESSAGE,
    )


def email_verified(user: dict = Depends(get_current_user)) -> dict:
    if user["is_email_verified"]:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=EMIL_NOT_VERIFIED_MESSAGE,
    )
