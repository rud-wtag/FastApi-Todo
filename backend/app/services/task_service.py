from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi_pagination import paginate
from sqlalchemy.orm import Session

from app.core.constants import ADMIN
from app.core.database import get_db
from app.models.task import Task
from app.models.user import User
from app.schema.task_schema import TaskCreateRequest, TaskUpdateRequest


class TaskService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_task(self, user: dict, create_task_request: TaskCreateRequest):
        new_task = Task(**create_task_request.model_dump())
        new_task.user_id = user["id"]
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def get_all_tasks(self, search_query, category, status, user: dict):
        tasks = self.db.query(Task)
        if user["role"] != ADMIN:
            tasks = tasks.filter(Task.user_id == user["id"])
        if search_query:
            tasks = tasks.filter(Task.title.ilike(f"%{search_query}%"))
        if category:
            tasks = tasks.filter(Task.category == category)
        if status:
            tasks = tasks.filter(Task.status == status)
        if status == False:
            tasks = tasks.filter(Task.status == False)
        return paginate(tasks.order_by(Task.created_at.desc()).all())

    def get_all_tasks_by_user(self, user: dict):
        return (
            self.db.query(Task)
            .filter(Task.user == user["id"])
            .order_by(Task.id.asc())
            .all()
        )

    def get_task_by_id(self, user: dict, task_id: int):
        task = self.db.query(Task)
        task = task.filter(Task.id == task_id)
        if user["role"] != ADMIN:
            task = task.filter(Task.user_id == user["id"])
        task = task.first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        return task

    def update_task(
        self, user: dict, task_id: int, task_update_request: TaskUpdateRequest
    ):
        task = self.get_task_by_id(user, task_id)

        for field, value in task_update_request.model_dump().items():
            if hasattr(task, field):
                setattr(task, field, value)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid field: {field}",
                )

        task.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, user: User, task_id: int):
        task = self.get_task_by_id(user, task_id)
        self.db.delete(task)
        self.db.commit()
        return {"message": "Task deleted successfully"}

    def mark_as_complete(self, task_id: int, user: dict):
        task = self.get_task_by_id(user, task_id)

        if task is not None:
            task.status = True
            task.updated_at = datetime.now()
            task.completed_at = datetime.now()
            self.db.commit()
            self.db.refresh(task)
            return task

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not Found",
        )

    def mark_as_incomplete(self, task_id: int, user: dict):
        task = self.get_task_by_id(user, task_id)

        if task is not None:
            task.status = False
            task.updated_at = datetime.now()
            task.completed_at = None
            self.db.commit()
            self.db.refresh(task)
            return task

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not Found",
        )
