from sqlalchemy import Column, String

from app.db.base import Base
from app.models.base_model import BaseModel


class Role(Base, BaseModel):
    __tablename__ = "roles"

    name = Column(String(450), primary_key=True)
