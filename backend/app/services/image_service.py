import os
import shutil
from datetime import datetime

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings
from app.core.constants import IMAGE_SAVE_FAILED_MESSAGE


class ImageService:
    def __init__(self, directory: str = "files/"):
        self.directory = directory

    def save_image(self, image: UploadFile):
        now = str(datetime.now())[:19]
        now = now.replace(":", "_")
        filename, extension = os.path.splitext(image.filename)
        path = os.path.join(
            self.directory,
            f"{filename}_{now}{extension}",
        )
        try:
            with open(path, "wb+") as buffer:
                shutil.copyfileobj(image.file, buffer)
        except IOError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{IMAGE_SAVE_FAILED_MESSAGE} {str(e)}",
            )

        return path

    def get_file(self, path: str):
        return f"{settings.app.host}/{path}" if path else None


image_service = ImageService()
