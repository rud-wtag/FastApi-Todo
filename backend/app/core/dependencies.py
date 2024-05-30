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
    access_token: str = Cookie(None),
    jwt_token_service: JWTTokenInterface = Depends(JWTTokenService),
):
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=UNAUTHORIZE_MESSAGE
        )
    user = jwt_token_service.verify_token(access_token)

    return user


def admin(user: dict = Depends(get_current_user)):
    if user["role"] is not None and user["role"] == ADMIN:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UNAUTHORIZE_MESSAGE,
        )


def auth(user: dict = Depends(get_current_user)):
    if user["role"] is not None and user["role"] == ADMIN:
        return user
    if user["role"] is not None and user["role"] == USER:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UNAUTHORIZE_MESSAGE,
        )


def active_user(user: dict = Depends(get_current_user)):
    if user["is_active"] is not None and user["is_active"] is True:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UNAUTHORIZE_MESSAGE,
        )


def email_verified(user: dict = Depends(get_current_user)):
    if user["is_email_verified"] is not None and user["is_email_verified"] is True:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=EMIL_NOT_VERIFIED_MESSAGE,
        )
