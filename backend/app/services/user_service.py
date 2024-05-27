from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.interface.user_interface import UserInterface
from app.models.user import User


class UserService(UserInterface):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all_users(self):
        return self.db.query(User).all()

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def activate_user(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_active = True
            self.db.commit()
            return True
        else:
            return False

    def deactivate_user(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_active = False
            self.db.commit()
            return True
        else:
            return False

    def delete_user(self, user_id: int, current_user: dict):
        if int(user_id) == current_user["id"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You can not delete yourself",
            )

        user = self.get_user(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found",
            )
        self.db.delete(user)
        self.db.commit()
        return {"message": "User deleted successfully"}
