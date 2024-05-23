from datetime import datetime
from typing import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.constants import ADMIN
from app.core.constants import USER as ROLE_USER
from app.db.base import Base
from app.db.database import get_db
from app.faker.task_faker import create_dummy_tasks
from app.main import app
from app.models.role import Role
from app.models.task import Task
from app.models.user import User
from app.utils.helpers import get_hashed_password

if settings.app.env not in ["test"]:
    msg = f"ENV is not test, it is {settings.APP_ENV}"
    pytest.exit(msg)

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionTesting = sessionmaker(autoflush=False, autocommit=False, bind=engine)

USER = {"full_name": "Mr. A", "email": "demo@mail.com", "password": "secret"}

TASK = {
    "category": "Work",
    "description": "Finish the report",
    "due_date": "2024-05-30T00:00:00",
    "title": "Demo task title",
}


@pytest.fixture
def test_session() -> Generator:
    """Test database connection"""
    db = SessionTesting()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def app_test():
    Base.metadata.create_all(bind=engine)
    yield app
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(app_test, test_session):
    """Fixture for creating a FastAPI test client"""

    def _test_db():
        try:
            yield test_session
        finally:
            pass

    app_test.dependency_overrides[get_db] = _test_db
    return TestClient(app_test)


@pytest.fixture
def mock_db_session():
    return MagicMock()


@pytest.fixture
def insert_user_data(test_session):
    db = test_session

    def create_role():
        roles = [Role(id=1, name=ADMIN), Role(id=2, name=ROLE_USER)]
        db.add_all(roles)
        db.commit()

    create_role()
    role = db.query(Role).filter(Role.name == ADMIN).first()
    user = User(
        id=1,
        full_name=USER["full_name"],
        email=USER["email"],
        is_active=True,
        password=get_hashed_password(USER["password"]),
        role_id=role.id if role else None,
    )
    db.add(user)
    db.commit()


@pytest.fixture
def insert_task_data(test_session):
    db = test_session

    def create_role():
        role = Role(id=1, name=ADMIN)
        db.add(role)
        db.commit()

    create_role()
    role = db.query(Role).filter(Role.name == ADMIN).first()
    user = User(
        id=1,
        full_name=USER["full_name"],
        email=USER["email"],
        is_active=True,
        password=get_hashed_password(USER["password"]),
        role_id=role.id if role else None,
    )
    db.add(user)
    db.commit()

    new_task = Task(
        id=1,
        title=TASK["title"],
        category=TASK["category"],
        description=TASK["description"],
        due_date=datetime(TASK["due_date"]),
    )
    new_task.user_id = user.id
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    create_dummy_tasks(db, user.id, 100)
