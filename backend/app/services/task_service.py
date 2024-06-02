from datetime import datetime, timedelta

import pytz
from fastapi import Depends, HTTPException, status
from fastapi_pagination import paginate
from fastapi_utilities import repeat_at
from sqlalchemy import and_, create_engine
from sqlalchemy.orm import Session, sessionmaker
from starlette.background import BackgroundTasks

from app.core.config import settings
from app.core.constants import ADMIN, TASK_DELETED_MESSAGE, TASK_NOT_FOUND
from app.core.mail import mail
from app.db.crud import CRUDBase
from app.db.database import get_db
from app.logger import logger
from app.models.task import Task
from app.models.user import User
from app.schema.task_schema import TaskCreateRequest, TaskUpdateRequest


class TaskService(CRUDBase):
    def __init__(
        self,
        db: Session = Depends(get_db),
        background_tasks: BackgroundTasks = BackgroundTasks(),
    ):
        self.db = db
        self.background_tasks = background_tasks
        super().__init__(model=Task)

    def create_task(self, user: dict, create_task_request: TaskCreateRequest):
        create_task_request.user_id = user["id"]
        return self.create(db=self.db, obj_in=create_task_request)

    def get_all_tasks(
        self, search_query, category, priority_level, due_date, status, user: dict
    ):
        filters = []

        if user and user["role"] != ADMIN:
            filters.append(Task.user_id == user["id"])

        optional_filters = {
            Task.title.ilike(f"%{search_query}%"): search_query,
            Task.category == category: category,
            Task.priority_level == priority_level: priority_level,
            Task.due_date == datetime.fromisoformat(due_date)
            if due_date
            else None: due_date,
            Task.status == status: status is not None,
        }

        for condition, value in optional_filters.items():
            if value:
                filters.append(condition)

        tasks = self.db.query(Task).filter(and_(*filters))

        return paginate(tasks.order_by(Task.created_at.desc()).all())

    def get_all_tasks_by_user(self, user: dict):
        return self.get_multi_by_field(self.db, "user_id", user[id])

    def get_task_by_id(self, user: dict, task_id: int):
        task = self.db.query(Task).filter(Task.id == task_id)
        if user["role"] != ADMIN:
            task = task.filter(Task.user_id == user["id"])
        task = task.first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=TASK_NOT_FOUND
            )
        return task

    def update_task(
        self, user: dict, task_id: int, task_update_request: TaskUpdateRequest
    ):
        task = self.get_task_by_id(user, task_id)
        return self.update(db=self.db, obj_in=task_update_request, id=task.id)

    def delete_task(self, user: User, task_id: int):
        task = self.get_task_by_id(user, task_id)
        self.remove(db=self.db, id=task.id)
        return {"message": TASK_DELETED_MESSAGE}

    def mark_as_complete(self, task_id: int, user: dict):
        task = self.get_task_by_id(user, task_id)
        update_data = {"status": True, "completed_at": datetime.now()}
        task = self.update(db=self.db, obj_in=update_data, id=task.id)
        return task

    def mark_as_incomplete(self, task_id: int, user: dict):
        task = self.get_task_by_id(user, task_id)
        update_data = {"status": False, "completed_at": None}
        task = self.update(db=self.db, obj_in=update_data, id=task.id)
        return task

    # @repeat_at(cron="*/1 * * * *")
    @repeat_at(cron="0 1 * * *")
    async def send_mail_to_user_on_due_task(self):
        engine = create_engine(settings.database.url, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        try:
            tomorrow = datetime.now(pytz.utc) + timedelta(days=1)
            tomorrow_start = datetime(
                tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0, tzinfo=pytz.utc
            )
            tomorrow_end = datetime(
                tomorrow.year, tomorrow.month, tomorrow.day, 23, 59, 59, tzinfo=pytz.utc
            )

            # Filter tasks due tomorrow
            tasks_due_tomorrow = (
                db.query(Task)
                .filter(Task.due_date >= tomorrow_start, Task.due_date <= tomorrow_end)
                .all()
            )

            # Send email to each user with a task due tomorrow
            for task in tasks_due_tomorrow:
                user = db.query(User).filter(User.id == task.user_id).first()
                if user and user.email:
                    await mail.send_email_async(
                        "Remainder Email",
                        user.email,
                        "",
                        template_body={"task_id": task.id, "due_date": task.due_date},
                        template_name="task-remainder.html",
                    )
            logger.info(f"Remainder sent to task owner -> {task.id}")
        except Exception as e:
            logger.exception(e)
