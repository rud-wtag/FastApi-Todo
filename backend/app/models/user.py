from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import Base
from app.models.base_model import BaseModel
from app.models.role import Role


class User(Base, BaseModel):
    __tablename__ = "users"

    role_id = Column(Integer, ForeignKey(Role.id, ondelete="SET NULL"), nullable=True)
    role = relationship(Role)
    full_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    avatar = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
    is_email_verified = Column(Boolean, default=False)
