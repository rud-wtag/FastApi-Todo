import shutil
from datetime import datetime, timedelta

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User


class ImageService:
    def __init__(self, directory: str = "files/"):
        self.directory = directory

    def save_image(self, image: UploadFile):
        now = str(datetime.now())[:19]
        now = now.replace(":", "_")

        path = (
            self.directory
            + image.filename.split(".")[0]
            + now
            + "."
            + image.filename.split(".")[-1]
        )
        with open(path, "wb+") as buffer:
            shutil.copyfileobj(image.file, buffer)

        return path

    def get_file(self, path: str):
        return f"{settings.app.host}/{path}" if path else None


image_service = ImageService()
