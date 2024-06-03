from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.constants import (
    ACCESS_TOKEN,
    UNAUTHORIZE_MESSAGE,
    USER,
    USER_NOT_FOUND_MESSAGE,
)
from app.db.crud import CRUDBase
from app.db.database import get_db
from app.interface.jwt_token_interface import JWTTokenInterface
from app.models.token import Token
from app.models.user import User
from app.schema.token_schema import TokenCreate, TokenUpdate
from app.services.image_service import image_service
from app.utils.helpers import decode_token


class JWTTokenService(JWTTokenInterface, CRUDBase):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        super().__init__(model=Token)
        self.user_crud = CRUDBase(model=User)

    def store_token(self, user_id: int, token: str):
        token_create_data = TokenCreate(user_id=user_id, token=token)
        return self.create(db=self.db, obj_in=token_create_data)

    def blacklist_token(self, user_id: int, token: str) -> bool:
        token_model = self.get_by_fields(self.db, {"user_id": user_id, "token": token})
        if token_model:
            return self.update(
                db=self.db, obj_in=TokenUpdate(status=False), id=token_model.id
            )
        return False

    def is_blacklist_token(self, user_id: int, token: str) -> bool:
        token_model = self.get_by_fields(self.db, {"user_id": user_id, "token": token})
        return token_model and not token_model.status

    def create_token(
        self,
        email: str,
        id: int,
        validity: timedelta,
        type: str = ACCESS_TOKEN,
        role: str = USER,
    ):
        encode = {"sub": email, "id": id, "type": type, "role": role}
        expires = datetime.now() + validity
        encode.update({"exp": expires})
        token = jwt.encode(
            encode, settings.app.secret_key, algorithm=settings.app.algorithm
        )
        self.store_token(id, token)
        return token

    def verify_token(self, token: str):
        try:
            payload = decode_token(token)
            username = payload.get("sub")
            user_id = payload.get("id")
            token_type = payload.get("type")

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=UNAUTHORIZE_MESSAGE,
            )

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=UNAUTHORIZE_MESSAGE,
            )

        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=UNAUTHORIZE_MESSAGE,
            )

        if self.is_blacklist_token(user_id, token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=UNAUTHORIZE_MESSAGE,
            )

        user = self.user_crud.get(self.db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=USER_NOT_FOUND_MESSAGE,
            )

        return {
            "id": user_id,
            "username": username,
            "avatar": image_service.get_file(user.avatar),
            "full_name": user.full_name,
            "role": user.role.name,
            "is_email_verified": user.is_email_verified,
            "is_active": user.is_active,
            "token_type": token_type,
        }

    def refresh_token(self, refresh_token: str) -> str | bool:
        token_details = self.verify_token(refresh_token)

        if token_details is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=UNAUTHORIZE_MESSAGE,
            )
        access_token = self.create_token(
            token_details["username"],
            token_details["id"],
            timedelta(days=settings.app.access_token_validity),
        )
        return access_token


jwt_token_service = JWTTokenService()
