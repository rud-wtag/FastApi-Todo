from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.models.user import User


class UserInterface(ABC):
    """User registration interface to manage user credentials"""

    @abstractmethod
    def get_all_users(self, db: Session) -> list[User]:
        """Get all list of users"""
        pass

    @abstractmethod
    def get_user(self, db: Session, user_id: int) -> User | None:
        """Get user by user id"""
        pass

    @abstractmethod
    def activate_user(self, db: Session, user_id: int) -> bool:
        """Activate user by user id"""
        pass

    @abstractmethod
    def deactivate_user(self, db: Session, user_id: int) -> bool:
        """Deactivate user by user_id"""
        pass

    @abstractmethod
    def delete_user(self, db: Session, user_id: int) -> dict:
        """Delete user by user_id"""
        pass
