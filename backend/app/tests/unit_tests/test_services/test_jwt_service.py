from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from freezegun import freeze_time
from jose import jwt

from app.core.config import settings
from app.core.constants import UNAUTHORIZE_MESSAGE
from app.models.token import Token
from app.models.user import User
from app.schema.token_schema import TokenUpdate
from app.services.image_service import image_service
from app.services.jwt_token_service import jwt_token_service


class TestJwtTokenService:
    def setup_method(self):
        self.user = {"user_id": 1, "token": "test_token"}

    @patch("app.db.crud.CRUDBase.create")
    def test_store_token(self, mock_crud_base, mock_db_session):
        mock_crud_base.return_value = self.user
        jwt_token_service.store_token(
            mock_db_session, self.user.get("user_id"), self.user.get("token")
        )

        assert mock_crud_base.called
        # assert the token data is stored correctly
        args, kwargs = mock_crud_base.call_args
        token_create_data = kwargs["obj_in"]
        assert token_create_data.user_id == self.user.get("user_id")
        assert token_create_data.token == self.user.get("token")

    @pytest.mark.parametrize("token_db_value", [None, MagicMock(spec=Token)])
    def test_blacklist_token(self, token_db_value, mock_db_session):
        jwt_token_service.get_by_fields = MagicMock(return_value=token_db_value)
        jwt_token_service.update = MagicMock(return_value=True)

        result = jwt_token_service.blacklist_token(
            mock_db_session, self.user.get("user_id"), self.user.get("token")
        )

        jwt_token_service.get_by_fields.assert_called_with(
            mock_db_session,
            {"user_id": self.user.get("user_id"), "token": self.user.get("token")},
        )

        if not token_db_value:
            assert result is False
        else:
            jwt_token_service.update.assert_called_with(
                db=mock_db_session,
                obj_in=TokenUpdate(status=False),
                id=token_db_value.id,
            )
            assert result is True

    @pytest.mark.parametrize(
        "stored_db_token", [False, MagicMock(spec=Token, status=False)]
    )
    def test_is_blacklist_token(self, stored_db_token, mock_db_session):
        jwt_token_service.get_by_fields = MagicMock(return_value=stored_db_token)

        result = jwt_token_service.is_blacklist_token(
            mock_db_session, self.user.get("user_id"), self.user.get("token")
        )

        jwt_token_service.get_by_fields.assert_called_with(
            mock_db_session,
            {"user_id": self.user.get("user_id"), "token": self.user.get("token")},
        )

        if not stored_db_token:
            assert result is False
        else:
            assert result is True

    @freeze_time("2024-01-01")
    def test_create_token(self, mock_db_session):
        encode = {
            "sub": "a@b.com",
            "id": 1,
            "role": "user",
            "type": "access_token",
            "exp": datetime.now() + timedelta(days=1),
        }
        jwt_token_service.store_token = MagicMock()

        with patch.object(jwt, "encode", return_value="test_encoded_token"):
            token = jwt_token_service.create_token(
                db=mock_db_session,
                email=encode["sub"],
                id=encode["id"],
                validity=timedelta(days=1),
                type=encode["type"],
                role=encode["role"],
            )

            jwt.encode.assert_called()
            jwt.encode.assert_called_with(
                encode, settings.app.secret_key, algorithm=settings.app.algorithm
            )
            jwt_token_service.store_token.assert_called_with(
                mock_db_session, encode["id"], "test_encoded_token"
            )
            assert token == "test_encoded_token"

    @freeze_time("2024-01-01")
    def test_verify_token(self, mock_db_session):
        jwt_token_service.store_token = MagicMock()

        encode = {
            "sub": "a@b.com",
            "id": 1,
            "type": "access_token",
            "exp": datetime.now() + timedelta(days=1),
            "role": "admin",
        }

        user_data = {
            "full_name": "admin",
            "is_email_verified": True,
            "is_active": True,
        }

        jwt_token_service.is_blacklist_token = MagicMock(return_value=False)

        user = MagicMock(spec=User)
        user.role.name = encode["role"]
        user.full_name = user_data["full_name"]
        user.is_email_verified = user_data["is_email_verified"]
        user.is_active = user_data["is_active"]
        jwt_token_service.user_crud.get = MagicMock(return_value=user)

        with patch("app.services.jwt_token_service.decode_token", return_value=encode):
            payload = jwt_token_service.verify_token(
                db=mock_db_session, token="test_token"
            )

            assert payload["username"] == encode["sub"]
            assert payload["id"] == encode["id"]
            assert payload["role"] == encode["role"]
            assert jwt_token_service.is_blacklist_token.call_args[0] == (
                mock_db_session,
                encode["id"],
                "test_token",
            )

            jwt_token_service.user_crud.get.assert_called_with(
                mock_db_session, encode["id"]
            )

            assert payload["avatar"] == image_service.get_file(user.avatar)
            assert payload["full_name"] == user.full_name
            assert payload["is_email_verified"] == user.is_email_verified
            assert payload["is_active"] == user.is_active
            assert payload["token_type"] == encode["type"]

    @freeze_time("2024-01-01")
    def test_verify_token_blacklisted(self, mock_db_session):
        encode = {
            "sub": "a@b.com",
            "id": 1,
            "type": "access_token",
            "exp": datetime.now() + timedelta(days=1),
            "role": "admin",
        }
        with patch("app.utils.helpers.decode_token", return_value=encode):
            jwt_token_service.is_blacklist_token = MagicMock(return_value=True)

            with pytest.raises(HTTPException) as exc_info:
                jwt_token_service.verify_token(db=mock_db_session, token="test_token")

            assert exc_info.value.status_code == 401
            assert exc_info.value.detail == UNAUTHORIZE_MESSAGE

    # @freeze_time("2024-01-01")
    # def test_verify_token_user_not_found(self, mock_db_session):
    #

    #     encode = {
    #         "sub": "a@b.com",
    #         "id": 1,
    #         "type": "access_token",
    #         "exp": datetime.now() + timedelta(days=1),
    #         "role": "admin",
    #     }

    #     # Mock decode_token to return the encoded payload
    #     with patch("app.utils.helpers.decode_token", return_value=encode):
    #         # Mock is_blacklist_token to return False
    #         jwt_token_service.is_blacklist_token = MagicMock(return_value=False)

    #         # Mock user_crud.get to return None
    #         jwt_token_service.user_crud.get = MagicMock(return_value=None)

    #         with pytest.raises(HTTPException) as exc_info:
    #             jwt_token_service.verify_token(db=mock_db_session, token="test_token")
    #         assert exc_info.value.status_code == 401
    #         assert exc_info.value.detail == USER_NOT_FOUND_MESSAGE

    def test_refresh_token(self, mock_db_session):
        encode = {
            "sub": "a@b.com",
            "id": 1,
            "type": "access_token",
            "exp": datetime.now() + timedelta(days=1),
            "role": "admin",
        }

        with patch.object(
            jwt_token_service,
            "verify_token",
            return_value={
                "username": encode["sub"],
                "id": encode["id"],
                "role": encode["role"],
            },
        ):
            jwt_token_service.create_token = MagicMock(return_value="test_token")
            res = jwt_token_service.refresh_token(mock_db_session, "test_token")
            assert res == "test_token"

        with pytest.raises(HTTPException) as exc_info:
            with patch.object(jwt_token_service, "verify_token", return_value=None):
                jwt_token_service.refresh_token(mock_db_session, "test_token")
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == UNAUTHORIZE_MESSAGE
