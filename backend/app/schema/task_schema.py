from datetime import datetime, timedelta
from typing import Optional

import pytz
from pydantic import BaseModel, Field, computed_field, field_validator
from pydantic_core import PydanticCustomError

from app.schema.base_schema import ModelBaseInfo


class Task(ModelBaseInfo, BaseModel):
    user_id: int
    title: str
    category: str
    description: str
    status: bool
    priority_level: str
    due_date: datetime
    completed_at: Optional[datetime]

    class Config:
        orm_mode: True

    @computed_field
    @property
    def task_state(self) -> str:
        current_time = datetime.now(pytz.utc)  # Ensure current time is timezone-aware
        if self.due_date.tzinfo is None:
            current_time = datetime.now()
        if self.completed_at:
            if self.completed_at < self.due_date:
                return "complete"
            else:
                return "outdated"
        if self.due_date < current_time:
            return "outdated"
        return "incomplete"


class TaskCreateRequest(BaseModel):
    title: str = Field(min_length=3)
    category: str = Field(min_length=3)
    description: str = Field(min_length=1)
    priority_level: Optional[str] = "LOW"
    due_date: datetime = Field(default=datetime.now() + timedelta(days=1))

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, due_time: datetime) -> datetime:
        if due_time.tzinfo is None:
            due_time = pytz.utc.localize(
                due_time
            )  # Convert naive datetime to aware datetime in UTC
        if due_time < datetime.now(pytz.utc):
            raise PydanticCustomError(
                "date error",
                f"{due_time} is behind the current date",
                {"date": due_time},
            )
        return due_time

    class Config:
        extra = "allow"
        json_schema_extra = {
            "example": {
                "title": "Demo task title",
                "category": "Work",
                "description": "Finish the report",
                "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
            }
        }


class TaskUpdateRequest(BaseModel):
    title: Optional[str]
    category: Optional[str]
    description: Optional[str]
    priority_level: Optional[str]
    due_date: Optional[datetime]

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, due_time: datetime) -> datetime:
        if due_time.tzinfo is None:
            due_time = pytz.utc.localize(
                due_time
            )  # Convert naive datetime to aware datetime in UTC
        if due_time < datetime.now(pytz.utc):
            raise PydanticCustomError(
                "date error",
                f"{due_time} is behind the current date",
                {"date": due_time},
            )
        return due_time

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Demo task title",
                "category": "Work",
                "description": "Finish the report",
                "priority_level": "High",
                "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
            }
        }
    }
