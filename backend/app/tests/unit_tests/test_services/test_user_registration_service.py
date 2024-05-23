from unittest.mock import MagicMock, patch

import pytest

from app.core.constants import ACCESS_TOKEN, ADMIN, REFRESH_TOKEN
from app.models.user import User
from app.schema.auth_schema import CreateUserRequest
from app.services.auth_service import AuthService
from app.services.jwt_token_service import JWTTokenService
from app.services.user_registration_service import UserRegistrationService


class TestAuthService:
    def setup_method(self):
        self.user = {
            "id": 1,
            "username": "test@mail.com",
            "full_name": "Mr. A",
            "role": ADMIN,
            "token": "test_token",
        }

    @pytest.mark.skip(reason="will implement later")
    @patch("app.services.auth_service.User")
    def test_send_verification_mail(
        self,
        mock_user_class,
        mock_db_session,
    ):
        mock_jwt_token_service = MagicMock(JWTTokenService)
        user_registration_service = UserRegistrationService(
            db=mock_db_session, jwt_token_service=mock_jwt_token_service
        )
        mock_user_class.return_value = self.user
        mock_db_session.query().filter().first.return_value = self.user
        mock_db_session.commit.return_value = self.user

        user_registration_service.send_verification_mail(
            self.user["username"], self.user["id"]
        )
