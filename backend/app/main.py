import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination

from app.api.v1.routes import routers
from app.core.config import settings

if not os.path.exists(settings.app.asset_directory):
    os.makedirs(settings.app.asset_directory)

app = FastAPI()
add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=settings.cors.origins,
    allow_methods=settings.cors.methods,
    allow_headers=settings.cors.headers,
)

app.mount("/files", StaticFiles(directory=settings.app.asset_directory), name="files")

app.include_router(routers, prefix="/api/v1")
