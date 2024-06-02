from typing import Annotated

from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError

from app.core.constants import (
    EMAIL_INVALID_MESSAGE,
    LOGGED_IN_MESSAGE,
    PASSWORD_RESET_MESSAGE,
    TOKEN_REFRESH_MESSAGE,
)
from app.core.dependencies import get_current_user
from app.interface.user_registration_interface import UserRegistrationInterface
from app.schema.auth_schema import (
    CreateUserRequest,
    CreateUserResponse,
    LoginResponse,
    ProfileUpdateRequest,
    UserProfileResponse,
)
from app.schema.response_schema import SuccessResponse
from app.services.auth_service import AuthInterface, AuthService
from app.services.image_service import image_service
from app.services.jwt_token_service import JWTTokenInterface, JWTTokenService
from app.services.user_registration_service import UserRegistrationService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register", response_model=CreateUserResponse, status_code=status.HTTP_200_OK
)
def register(
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(..., min_length=6),
    avatar: UploadFile = File(default=None),
    auth_service: AuthInterface = Depends(AuthService),
):
    avatar_path = None
    if avatar:
        avatar_path = image_service.save_image(avatar)
    try:
        create_user_request = CreateUserRequest(
            full_name=full_name, email=email, password=password, avatar=avatar_path
        )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=EMAIL_INVALID_MESSAGE,
        )
    user = auth_service.registration(create_user_request=create_user_request)
    return user


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthInterface = Depends(AuthService),
):
    tokens = auth_service.login(form_data.username, form_data.password)
    response = JSONResponse({"msg": LOGGED_IN_MESSAGE, "user": tokens["user"]})
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=True,
        samesite="none",
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="none",
    )
    return response


@router.get(
    "/profile", response_model=UserProfileResponse, status_code=status.HTTP_200_OK
)
def profile(user: dict = Depends(get_current_user)):
    return user


@router.post(
    "/update-profile", response_model=CreateUserResponse, status_code=status.HTTP_200_OK
)
def update_profile(
    profile_update_request: ProfileUpdateRequest,
    user: dict = Depends(get_current_user),
    auth_service: AuthInterface = Depends(AuthService),
):
    updated_user = auth_service.profile_update(user["id"], profile_update_request)
    return updated_user


@router.get(
    "/send-verification-email",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
def send_verify_email(
    user: dict = Depends(get_current_user),
    user_registration_service: UserRegistrationInterface = Depends(
        UserRegistrationService
    ),
):
    response = user_registration_service.send_verification_mail(
        user["username"], user["id"]
    )
    return response


@router.get("/verify-email", status_code=status.HTTP_200_OK)
def verify_email(
    token: str,
    request: Request,
    user_registration_service: UserRegistrationInterface = Depends(
        UserRegistrationService
    ),
):
    template = user_registration_service.verify_email(token, request)
    return template


@router.post("/refresh_token", status_code=status.HTTP_200_OK)
def refresh_token(
    jwt_token_service: JWTTokenInterface = Depends(JWTTokenService),
    refresh_token: str = Cookie(None),
):
    access_token = jwt_token_service.refresh_token(refresh_token)
    response = JSONResponse({"message": TOKEN_REFRESH_MESSAGE})
    response.set_cookie(
        key="access_token", value=access_token, httponly=True, secure=True
    )
    return response


@router.post(
    "/send-password-reset-link",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
def password_reset_link(
    email: Annotated[str, Form()],
    user_registration_service: UserRegistrationInterface = Depends(
        UserRegistrationService
    ),
):
    response = user_registration_service.send_reset_password_link(email)
    return response


@router.post("/reset-password", status_code=status.HTTP_200_OK)
def password_reset(
    token: str,
    new_password: Annotated[str, Form()],
    user_registration_service: UserRegistrationInterface = Depends(
        UserRegistrationService
    ),
):
    user_registration_service.reset_password(token, new_password)
    response = JSONResponse({"message": PASSWORD_RESET_MESSAGE})
    response.delete_cookie(
        key="access_token", samesite="none", secure=True, httponly=True
    )
    response.delete_cookie(
        key="refresh_token", samesite="none", secure=True, httponly=True
    )
    return response


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    old_password: Annotated[str, Form()],
    new_password: Annotated[str, Form()],
    user: dict = Depends(get_current_user),
    user_registration_service: UserRegistrationInterface = Depends(
        UserRegistrationService
    ),
):
    user_registration_service.change_password(new_password, old_password, user)
    response = JSONResponse({"message": PASSWORD_RESET_MESSAGE})
    response.delete_cookie(
        key="access_token", samesite="none", secure=True, httponly=True
    )
    response.delete_cookie(
        key="refresh_token", samesite="none", secure=True, httponly=True
    )
    return response


@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    user: dict = Depends(get_current_user),
    access_token: str = Cookie(None),
    refresh_token: str = Cookie(None),
    auth_service: AuthInterface = Depends(AuthService),
):
    return auth_service.logout(user["id"], access_token, refresh_token)
