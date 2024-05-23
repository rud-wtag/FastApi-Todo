from datetime import datetime

from faker import Faker
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.task import Task


def create_dummy_tasks(db: Session, user_id: int = 2, num_tasks: int = 1000):
    """Creates dummy tasks in the database for a specific user.

    Args:
        db_session: The database session object.
        user_id: The ID of the user to associate the tasks with.
        num_tasks: The number of tasks to create (defaults to 1000).
    """

    faker = Faker()

    for _ in range(num_tasks):
        task = Task(
            user_id=user_id,
            title=faker.sentence(),
            category=faker.word(),
            description=faker.paragraph(),
            status=faker.boolean(),
            priority_level=faker.random.choice(["LOW", "MEDIUM", "HIGH"]),
            created_at=datetime(2024, 5, 1),
            due_date=faker.date_between_dates(
                date_start=datetime(2024, 5, 10), date_end=datetime(2024, 5, 30)
            ),
        )
        db.add(task)

    db.commit()
