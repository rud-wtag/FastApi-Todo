from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.constants import (
    USER_DELETE_MESSAGE,
    USER_SELF_DELETE_MESSAGE,
)
from app.db.crud import CRUDBase
from app.interface.user_interface import UserInterface
from app.models.user import User


class UserService(UserInterface, CRUDBase):
    def __init__(self):
        super().__init__(model=User)

    def get_all_users(self, db: Session):
        return self.get_multi(db)

    def get_user(self, db: Session, user_id: int):
        return self.get(db, user_id)

    def activate_user(self, db: Session, user_id: int):
        update_data = {"id": user_id, "is_active": True}
        user = self.update(db=db, obj_in=update_data, id=user_id)
        return user

    def deactivate_user(self, db: Session, user_id: int):
        update_data = {"is_active": False}
        user = self.update(db=db, obj_in=update_data, id=user_id)
        return user

    def delete_user(self, db: Session, user_id: int, current_user: dict):
        if int(user_id) == current_user["id"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_SELF_DELETE_MESSAGE,
            )

        self.remove(db=db, id=user_id)

        return {"message": USER_DELETE_MESSAGE}


user_service = UserService()
