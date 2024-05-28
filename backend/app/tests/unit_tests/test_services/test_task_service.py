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
from app.services.task_service import TaskService
from app.models.task import Task


class TestTaskService:
    def setup_method(self):
        self.user = {
            "id": 1,
            "email": "test@mail.com",
            "full_name": "Mr. A",
            "role": ADMIN,
            "is_email_verified": False,
        }
        self.task = {
            "id": 1,
            "user_id": 1,
            "title": "string",
            "category": "string",
            "description": "string",
            "status": True,
            "priority_level": "string",
            "due_date": "2024-05-28",
            "completed_at": "2024-05-28",
        }
        self.token = "test_token"
        self.background_task = BackgroundTasks()

    @freeze_time("2024-01-1")
    @patch("app.services.user_registration_service.Task")
    def test_get_all_tasks(
        self,
        mock_task_class,
        mock_db_session,
    ):
        user_registration_service = TaskService(
            db=mock_db_session,
            background_tasks=self.background_task,
        )
        mock_task = Task(**self.task)
        mock_task_class.return_value = mock_task
        mock_db_session.query().filter().first.return_value = mock_task
        mock_db_session.commit.return_value = self.user
        url = f"{settings.app.frontend_url}/reset-password?token={self.token}"

        user_registration_service.get_all_tasks(self.user["email"])