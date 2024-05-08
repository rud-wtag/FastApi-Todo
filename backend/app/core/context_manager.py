from contextvars import ContextVar

from sqlalchemy.orm import Session

context_db_session: ContextVar[Session] = ContextVar("db_session", default=None)
context_set_db_session_rollback: ContextVar[bool] = ContextVar(
    "set_db_session_rollback", default=False
)
