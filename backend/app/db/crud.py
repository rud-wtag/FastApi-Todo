from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from app.db.base import Base
from app.logger import logger

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, *, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_by_field(self, db: Session, field: str, value: Any) -> Optional[ModelType]:
        if not hasattr(self.model, field):
            raise AttributeError(
                f"'{self.model.__name__}' object has no attribute '{field}'"
            )
        return db.query(self.model).filter(getattr(self.model, field) == value).first()

    def get_by_fields(
        self, db: Session, field_values: Dict[str, Any]
    ) -> Optional[ModelType]:
        filters = []
        for field, value in field_values.items():
            if not hasattr(self.model, field):
                raise AttributeError(
                    f"'{self.model.__name__}' object has no attribute '{field}'"
                )
            filters.append(getattr(self.model, field) == value)
        return db.query(self.model).filter(and_(*filters)).first()

    def get_multi_by_field(
        self, db: Session, field: str, value: Any
    ) -> Optional[ModelType]:
        return db.query(self.model).filter(getattr(self.model, field) == value).all()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, obj_in: Union[UpdateSchemaType, Dict[str, Any]], id: int
    ) -> ModelType:
        db_obj = db.query(self.model).get(id)
        if not db_obj:
            logger.error(f"{self.model.__name__} not found with id: {id}")
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, f"{self.model.__name__} not found"
            )
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        if not obj:
            logger.error(f"{self.model.__name__} not found with id: {id}")
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, f"{self.model.__name__} not found"
            )
        db.delete(obj)
        db.commit()
        return obj
