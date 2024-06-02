from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.constants import (
    EMAIL_ALREADY_EXIST,
    FAILED_TO_REGISTER,
    GUEST,
    INVALID_CREDENTIAL,
    LOGGED_OUT_MESSAGE,
    REFRESH_TOKEN,
    USER,
)
from app.db.crud import CRUDBase
from app.db.database import get_db
from app.interface.auth_interface import AuthInterface
from app.interface.jwt_token_interface import JWTTokenInterface
from app.interface.user_registration_interface import UserRegistrationInterface
from app.models.role import Role
from app.models.user import User
from app.schema.auth_schema import CreateUserRequest, ProfileUpdateRequest, RoleCreate
from app.services.jwt_token_service import JWTTokenService
from app.services.user_registration_service import UserRegistrationService
from app.utils.helpers import get_hashed_password, verify_password


class AuthService(AuthInterface, CRUDBase):
    def __init__(
        self,
        db: Session = Depends(get_db),
        jwt_token_service: JWTTokenInterface = Depends(JWTTokenService),
        user_registration_service: UserRegistrationInterface = Depends(
            UserRegistrationService
        ),
    ):
        self.jwt_token_service = jwt_token_service
        self.db = db
        self.user_registration_service = user_registration_service
        self.role_crud = CRUDBase(model=Role)
        super().__init__(model=User)

    def save_role(self, user_role: str = GUEST):
        self.role_crud.create(self.db, RoleCreate(user_role))

    def registration(self, create_user_request: CreateUserRequest) -> User:
        try:
            role = self.role_crud.get_by_field(self.db, "name", USER)
            create_user_request.role_id = role.id if role else None
            create_user_request.password = get_hashed_password(
                create_user_request.password
            )
            user = self.create(db=self.db, obj_in=create_user_request)
            self.user_registration_service.send_verification_mail(user.email, user.id)
        except IntegrityError as e:
            if "unique constraint" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=EMAIL_ALREADY_EXIST,
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=FAILED_TO_REGISTER,
                )
        return user

    def profile_update(self, user_id, profile_update_request: ProfileUpdateRequest):
        if profile_update_request.email:
            profile_update_request.is_email_verified = False
            self.user_registration_service.send_verification_mail(
                profile_update_request.email, user_id
            )

        return self.update(db=self.db, obj_in=profile_update_request, id=user_id)

    def login(self, email: str, password: str) -> dict:
        user = self.get_by_field(self.db, "email", email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INVALID_CREDENTIAL,
            )
        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INVALID_CREDENTIAL,
            )
        access_token = self.jwt_token_service.create_token(
            user.email, user.id, timedelta(days=1)
        )

        refresh_token = self.jwt_token_service.create_token(
            user.email, user.id, timedelta(days=7), type=REFRESH_TOKEN
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.full_name,
                "role": user.role.name,
            },
        }

    def logout(self, user_id, access_token: str, refresh_token: str):
        response = JSONResponse(
            {"message": LOGGED_OUT_MESSAGE}, status_code=status.HTTP_204_NO_CONTENT
        )
        response.delete_cookie(
            key="access_token", samesite="none", secure=True, httponly=True
        )
        response.delete_cookie(
            key="refresh_token", samesite="none", secure=True, httponly=True
        )
        self.jwt_token_service.blacklist_token(user_id, access_token)
        self.jwt_token_service.blacklist_token(user_id, refresh_token)
        return response


auth_service = AuthService()
