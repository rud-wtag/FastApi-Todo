from abc import ABC, abstractmethod

from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models.user import User
from app.schema.auth_schema import CreateUserRequest, ProfileUpdateRequest


class AuthInterface(ABC):
    """Auth interface to implement authentication"""

    @abstractmethod
    def registration(self, db: Session, create_user_request: CreateUserRequest) -> User:
        """
        Registration function that will implement child class

        **Parameters**
        * `create_user_request`: A CreateUserRequest pydentic request object

        **Returns**
        * `user`: A User type sqlalchemy model instance
        """
        pass

    @abstractmethod
    def profile_update(
        self, db: Session, user_id, profile_update_request: ProfileUpdateRequest
    ):
        """
        Registration function that will implement child class

        **Parameters**
        * `create_user_request`: A CreateUserRequest pydentic request object

        **Returns**
        * `user`: A User type sqlalchemy model instance
        """
        pass

    @abstractmethod
    def login(self, db: Session, email: str, password: str) -> dict:
        """
        login function that will implement child class

        **Parameters**
        * `email`: User email as string
        * `password`: User password as string
        """
        pass

    @abstractmethod
    def logout(
        self, db: Session, user_id: int, access_token: str, refresh_token: str
    ) -> JSONResponse:
        """
        login function that will implement child class

        **Parameters**
        * `user`: user id as integer
        * `schema`: A Pydantic model (schema) class
        """
        pass
