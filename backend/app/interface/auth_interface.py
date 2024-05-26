from abc import ABC, abstractmethod

from fastapi.responses import JSONResponse

from app.models.user import User
from app.schema.auth_schema import CreateUserRequest


class AuthInterface(ABC):
    """Auth interface to implement authentication"""

    @abstractmethod
    def registration(self, create_user_request: CreateUserRequest) -> User:
        """
        Registration function that will implement child class

        **Parameters**
        * `create_user_request`: A CreateUserRequest pydentic request object

        **Returns**
        * `user`: A User type sqlalchemy model instance
        """
        pass

    @abstractmethod
    def login(self, email: str, password: str) -> dict:
        """
        login function that will implement child class

        **Parameters**
        * `email`: User email as string
        * `password`: User password as string
        """
        pass

    @abstractmethod
    def logout(
        self, user_id: int, access_token: str, refresh_token: str
    ) -> JSONResponse:
        """
        login function that will implement child class

        **Parameters**
        * `user`: user id as integer
        * `schema`: A Pydantic model (schema) class
        """
        pass
