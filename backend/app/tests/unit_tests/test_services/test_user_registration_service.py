from datetime import timedelta
from unittest.mock import MagicMock, patch

from fastapi import Request
from freezegun import freeze_time
from starlette.background import BackgroundTasks

from app.core.config import settings
from app.core.constants import (
    ACCESS_TOKEN,
    ADMIN,
    EMAIL_VERIFICATION_TOKEN,
    RESET_PASSWORD_TOKEN,
)
from app.models.user import User
from app.services.jwt_token_service import JWTTokenService
from app.services.user_registration_service import UserRegistrationService


class TestUserRegistrationService:
    def setup_method(self):
        self.user = {
            "id": 1,
            "email": "test@mail.com",
            "full_name": "Mr. A",
            "role": ADMIN,
            "is_email_verified": False,
        }
        self.token = "test_token"
        self.background_task = BackgroundTasks()

    @freeze_time("2024-01-1")
    @patch("app.services.user_registration_service.User")
    @patch("app.services.user_registration_service.mail")
    def test_send_verification_mail(
        self,
        mock_mail_service,
        mock_user_class,
        mock_db_session,
    ):
        mock_jwt_token_service = MagicMock(JWTTokenService)
        user_registration_service = UserRegistrationService(
            db=mock_db_session,
            jwt_token_service=mock_jwt_token_service,
            background_tasks=self.background_task,
        )
        mock_user = User(**self.user)
        mock_user_class.return_value = mock_user
        mock_db_session.query().filter().first.return_value = mock_user
        mock_db_session.commit.return_value = self.user
        mock_jwt_token_service.create_token.return_value = self.token
        url = f"{settings.app.host}/api/v1/auth/verify-email?token={self.token}"

        user_registration_service.send_verification_mail(
            self.user["email"], self.user["id"]
        )

        mock_jwt_token_service.create_token.assert_called_with(
            self.user["email"],
            self.user["id"],
            timedelta(minutes=30),
            EMAIL_VERIFICATION_TOKEN,
        )
        mock_mail_service.send_email_background.assert_called_once_with(
            self.background_task,
            "Verify Email",
            self.user["email"],
            "",
            template_body={"url": url, "email": self.user["email"]},
            template_name="email-verification.html",
        )

    @patch("app.services.user_registration_service.User")
    @patch("app.services.user_registration_service.get_html")
    def test_verify_email(
        self,
        mock_get_html,
        mock_user_class,
        mock_db_session,
    ):
        mock_jwt_token_service = MagicMock(JWTTokenService)
        user_registration_service = UserRegistrationService(
            db=mock_db_session,
            jwt_token_service=mock_jwt_token_service,
            background_tasks=self.background_task,
        )
        mock_user = User(**self.user)
        mock_user_class.return_value = mock_user
        mock_db_session.query().filter().first.return_value = mock_user
        mock_jwt_token_service.verify_token.return_value = {
            "id": self.user["id"],
            "token_type": EMAIL_VERIFICATION_TOKEN,
        }
        request = MagicMock(spec=Request)

        reponse = user_registration_service.verify_email(self.token, request)

        mock_db_session.query.assert_called_with(mock_user_class)
        # mock_db_session.query().filter.assert_called_with(User.id == self.user['id'])
        mock_get_html.assert_called_once
        mock_get_html().TemplateResponse.assert_called_once_with(
            "email-verification-success.html",
            {"request": request, "msg": "Email verified successfully"},
        )

        mock_user_class.is_email_verified.return_value = True

        reponse = user_registration_service.verify_email(self.token, request)

        mock_get_html().TemplateResponse.assert_called_with(
            "email-verification-success.html",
            {"request": request, "msg": "Email already verified!"},
        )

    @freeze_time("2024-01-1")
    @patch("app.services.user_registration_service.User")
    @patch("app.services.user_registration_service.mail")
    def test_send_reset_password_link(
        self,
        mock_mail_service,
        mock_user_class,
        mock_db_session,
    ):
        mock_jwt_token_service = MagicMock(JWTTokenService)
        user_registration_service = UserRegistrationService(
            db=mock_db_session,
            jwt_token_service=mock_jwt_token_service,
            background_tasks=self.background_task,
        )
        mock_user = User(**self.user)
        mock_user_class.return_value = mock_user
        mock_db_session.query().filter().first.return_value = mock_user
        mock_db_session.commit.return_value = self.user
        mock_jwt_token_service.create_token.return_value = self.token
        url = f"{settings.app.frontend_url}/reset-password?token={self.token}"

        user_registration_service.send_reset_password_link(self.user["email"])

        mock_jwt_token_service.create_token.assert_called_once_with(
            self.user["email"],
            self.user["id"],
            timedelta(minutes=30),
            RESET_PASSWORD_TOKEN,
        )
        mock_mail_service.send_email_background(
            self.background_task,
            "Password reset email",
            self.user["email"],
            "",
            template_body={"url": url, "email": self.user["email"]},
            template_name="forget-password.html",
        )

    @patch("app.services.user_registration_service.User")
    @patch("app.services.user_registration_service.get_hashed_password")
    def test_reset_password(
        self,
        mock_get_hashed_password,
        mock_user_class,
        mock_db_session,
    ):
        mock_jwt_token_service = MagicMock(JWTTokenService)
        user_registration_service = UserRegistrationService(
            db=mock_db_session,
            jwt_token_service=mock_jwt_token_service,
            background_tasks=self.background_task,
        )
        mock_user = User(**self.user)
        mock_user_class.return_value = mock_user
        mock_db_session.query().filter().first.return_value = mock_user
        mock_jwt_token_service.verify_token.return_value = {
            "id": self.user["id"],
            "token_type": RESET_PASSWORD_TOKEN,
        }

        response = user_registration_service.reset_password(self.token, "new_password")

        mock_db_session.query.assert_called_with(mock_user_class)
        mock_get_hashed_password.assert_called_with("new_password")
        mock_db_session.commit.assert_called_once
        mock_db_session.refresh.assert_called_once
        mock_jwt_token_service.blacklist_token.assert_called_with(
            self.user["id"], self.token
        )
        assert response == {"message": "Password reset successful"}

    @patch("app.services.user_registration_service.User")
    @patch("app.services.user_registration_service.get_hashed_password")
    @patch("app.services.user_registration_service.verify_password")
    def test_change_password(
        self,
        mock_verify_password,
        mock_get_hashed_password,
        mock_user_class,
        mock_db_session,
    ):
        mock_jwt_token_service = MagicMock(JWTTokenService)
        user_registration_service = UserRegistrationService(
            db=mock_db_session,
            jwt_token_service=mock_jwt_token_service,
            background_tasks=self.background_task,
        )
        mock_user = User(**self.user)
        mock_user.password = "old_password"
        mock_user_class.return_value = mock_user
        mock_db_session.query().filter().first.return_value = mock_user
        mock_jwt_token_service.verify_token.return_value = {
            "id": self.user["id"],
            "token_type": ACCESS_TOKEN,
        }
        mock_user_class.password.return_value = "old_password"

        response = user_registration_service.change_password(
            "new_password",
            "old_password",
            {"id": self.user["id"], "token_type": ACCESS_TOKEN},
        )

        mock_db_session.query.assert_called_with(mock_user_class)
        mock_verify_password.assert_called_with("old_password", "old_password")
        mock_get_hashed_password.assert_called_with("new_password")
        mock_db_session.commit.assert_called_once
        mock_db_session.refresh.assert_called_once_with(mock_user)

        assert response == True
