from abc import ABC, abstractmethod

from fastapi import Request
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks


class UserRegistrationInterface(ABC):
    """User registration interface to manage user credentials"""

    @abstractmethod
    def send_verification_mail(
        self, db: Session, email: str, id: str, background_tasks: BackgroundTasks
    ):
        """send mail to the user"""
        pass

    @abstractmethod
    def verify_email(self, db: Session, token: str, request: Request):
        """verify email user email after with token"""
        pass

    @abstractmethod
    def send_reset_password_link(
        self, db: Session, email: str, background_tasks: BackgroundTasks
    ):
        """send reset password link to user email"""
        pass

    @abstractmethod
    def reset_password(self, db: Session, token: str, new_password: str):
        """reset password using reset password token"""
        pass

    @abstractmethod
    def change_password(
        self, db: Session, new_password: str, old_password: str, user: dict
    ):
        """change user password with personal access token"""
        pass
