from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.base_model import BaseModel
from app.models.user import User


class Token(Base, BaseModel):
    __tablename__ = "tokens"

    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=True)
    user = relationship(User, foreign_keys=[user_id])
    token = Column(String)
    status = Column(Boolean, default=True)
