from datetime import timedelta
from unittest.mock import MagicMock, patch

from fastapi import Request
from freezegun import freeze_time
from starlette.background import BackgroundTasks

from app.core.config import settings
from app.core.constants import (
    ACCESS_TOKEN,
    ADMIN,
    EMAIL_ALREADY_VERIFIED_MESSAGE,
    EMAIL_VERIFICATION_MAIL_SENT_MESSAGE,
    EMAIL_VERIFICATION_TOKEN,
    EMAIL_VERIFIED_MESSAGE,
    PASSWORD_RESET_MESSAGE,
    RESET_PASSWORD_TOKEN,
)
from app.models.user import User
from app.services.user_registration_service import user_registration_service


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
    @patch("app.services.user_registration_service.mail")
    @patch("app.services.user_registration_service.jwt_token_service")
    @patch("app.db.crud.CRUDBase.get_by_fields")
    def test_send_verification_mail(
        self,
        mock_crud_base,
        mock_jwt_token_service,
        mock_mail_service,
        mock_db_session,
    ):
        mock_user = User(**self.user)
        mock_crud_base.return_value = mock_user

        mock_jwt_token_service.create_token.return_value = self.token
        url = f"{settings.app.host}/api/v1/auth/verify-email?token={self.token}"

        response = user_registration_service.send_verification_mail(
            mock_db_session, self.user["email"], self.user["id"], self.background_task
        )

        mock_jwt_token_service.create_token.assert_called_with(
            mock_db_session,
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
        mock_crud_base.assert_called_once_with(mock_db_session, {"id": self.user["id"], "email":self.user['email']})
        assert response == {"message": EMAIL_VERIFICATION_MAIL_SENT_MESSAGE}

    @patch("app.services.user_registration_service.get_html")
    @patch("app.db.crud.CRUDBase.get")
    @patch("app.services.user_registration_service.jwt_token_service")
    def test_verify_email(
        self,
        mock_jwt_token_service,
        mock_crud_base,
        mock_get_html,
        mock_db_session,
    ):
        mock_user = User(**self.user)
        mock_crud_base.return_value = mock_user
        mock_jwt_token_service.verify_token.return_value = {
            "id": self.user["id"],
            "token_type": EMAIL_VERIFICATION_TOKEN,
        }
        request = MagicMock(spec=Request)

        user_registration_service.verify_email(mock_db_session, self.token, request)

        mock_db_session.commit.assert_called
        mock_db_session.refresh.assert_called_with(mock_user)
        # mock_db_session.query().filter.assert_called_with(User.id == self.user['id'])
        mock_get_html.assert_called_once
        mock_get_html().TemplateResponse.assert_called_once_with(
            "email-verification-success.html",
            {"request": request, "msg": EMAIL_VERIFIED_MESSAGE},
        )
        mock_user.is_email_verified = True
        mock_crud_base.return_value = mock_user

        user_registration_service.verify_email(mock_db_session, self.token, request)

        mock_get_html().TemplateResponse.assert_called_with(
            "email-verification-success.html",
            {"request": request, "msg": EMAIL_ALREADY_VERIFIED_MESSAGE},
        )

    @freeze_time("2024-01-1")
    @patch("app.services.user_registration_service.jwt_token_service")
    @patch("app.services.user_registration_service.mail")
    @patch("app.db.crud.CRUDBase.get_by_field")
    def test_send_reset_password_link(
        self,
        mock_crud_base,
        mock_mail_service,
        mock_jwt_token_service,
        mock_db_session,
    ):
        mock_user = User(**self.user)
        mock_crud_base.return_value = mock_user
        mock_jwt_token_service.create_token.return_value = self.token
        url = f"{settings.app.frontend_url}/reset-password?token={self.token}"

        user_registration_service.send_reset_password_link(
            mock_db_session, self.user["email"], self.background_task
        )

        mock_jwt_token_service.create_token.assert_called_once_with(
            mock_db_session,
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

    @patch("app.services.user_registration_service.jwt_token_service")
    @patch("app.services.user_registration_service.get_hashed_password")
    @patch("app.db.crud.CRUDBase.get")
    def test_reset_password(
        self,
        mock_crud_base,
        mock_get_hashed_password,
        mock_jwt_token_service,
        mock_db_session,
    ):
        mock_user = User(**self.user)
        mock_crud_base.return_value = mock_user
        mock_jwt_token_service.verify_token.return_value = {
            "id": self.user["id"],
            "token_type": RESET_PASSWORD_TOKEN,
        }

        response = user_registration_service.reset_password(
            mock_db_session, self.token, "new_password"
        )

        mock_get_hashed_password.assert_called_with("new_password")
        mock_db_session.commit.assert_called_once
        mock_db_session.refresh.assert_called_once
        mock_jwt_token_service.blacklist_token.assert_called_with(
            mock_db_session, self.user["id"], self.token
        )
        assert response == {"message": PASSWORD_RESET_MESSAGE}

    @patch("app.services.user_registration_service.jwt_token_service")
    @patch("app.services.user_registration_service.get_hashed_password")
    @patch("app.services.user_registration_service.verify_password")
    @patch("app.db.crud.CRUDBase.get")
    def test_change_password(
        self,
        mock_crud_base,
        mock_verify_password,
        mock_get_hashed_password,
        mock_jwt_token_service,
        mock_db_session,
    ):
        mock_user = User(**self.user)
        mock_user.password = "old_password"
        mock_crud_base.return_value = mock_user
        mock_db_session.query().filter().first.return_value = mock_user
        mock_jwt_token_service.verify_token.return_value = {
            "id": self.user["id"],
            "token_type": ACCESS_TOKEN,
        }

        mock_user.password = "old_password"

        response = user_registration_service.change_password(
            mock_db_session,
            "new_password",
            "old_password",
            {"id": self.user["id"], "token_type": ACCESS_TOKEN},
        )

        mock_verify_password.assert_called_with("old_password", "old_password")
        mock_get_hashed_password.assert_called_with("new_password")
        mock_crud_base.assert_called_once
        mock_crud_base.assert_called_once_with(mock_db_session, self.user["id"])

        assert response is True
