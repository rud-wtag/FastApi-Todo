from contextlib import asynccontextmanager
from typing import Optional

from fastapi import APIRouter, Depends, FastAPI, status
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app.core.constants import TASK_CREATED
from app.core.dependencies import auth, get_current_user
from app.db.database import get_db
from app.faker.task_faker import create_dummy_tasks
from app.schema.response_schema import SuccessResponse
from app.schema.task_schema import Task, TaskCreateRequest, TaskUpdateRequest
from app.services.task_service import task_service

router = APIRouter(prefix="", tags=["Tasks"], dependencies=[Depends(auth)])


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_request: TaskCreateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Task:
    return task_service.create_task(db, current_user, task_request)


@router.get("/tasks", response_model=Page[Task], status_code=status.HTTP_200_OK)
def get_all_tasks(
    search_query: Optional[str] = None,
    category: Optional[str] = None,
    priority_level: Optional[str] = None,
    due_date: Optional[str] = None,
    status: Optional[bool] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Page[Task]:
    tasks = task_service.get_all_tasks(
        db, search_query, category, priority_level, due_date, status, current_user
    )
    return tasks


@router.get("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def get_task_by_id(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Task:
    return task_service.get_task_by_id(db, current_user, task_id)


@router.put("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_task(
    task_id: int,
    update_task_request: TaskUpdateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Task:
    return task_service.update_task(db, current_user, task_id, update_task_request)


@router.put(
    "/tasks/{task_id}/complete", response_model=Task, status_code=status.HTTP_200_OK
)
def mark_as_complete(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Task:
    return task_service.mark_as_complete(db, task_id, current_user)


@router.put(
    "/tasks/{task_id}/incomplete", response_model=Task, status_code=status.HTTP_200_OK
)
def mark_as_incomplete(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Task:
    return task_service.mark_as_incomplete(db, task_id, current_user)


@router.delete(
    "/tasks/{task_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK
)
def delete_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SuccessResponse:
    return task_service.delete_task(db, current_user, task_id)


@router.get(
    "/create-fake-tasks", response_model=SuccessResponse, status_code=status.HTTP_200_OK
)
def fake_tasks(db: Session = Depends(get_db)) -> SuccessResponse:
    create_dummy_tasks(db)
    return {"message": TASK_CREATED}


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield task_service.send_mail_to_user_on_due_task()
