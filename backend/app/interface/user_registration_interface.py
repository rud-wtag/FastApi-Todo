from abc import ABC, abstractmethod

from fastapi import Request


class UserRegistrationInterface(ABC):
    """User registration interface to manage user credentials"""

    @abstractmethod
    def send_verification_mail(self, email: str, id: str):
        """send mail to the user"""
        pass

    @abstractmethod
    def verify_email(self, token: str, request: Request):
        """verify email user email after with token"""
        pass

    @abstractmethod
    def send_reset_password_link(self, email: str):
        """send reset password link to user email"""
        pass

    @abstractmethod
    def reset_password(self, token: str, new_password: str):
        """reset password using reset password token"""
        pass

    @abstractmethod
    def change_password(self, new_password: str, old_password: str, user: dict):
        """change user password with personal access token"""
        pass
