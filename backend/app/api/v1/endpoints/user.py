from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.core.constants import (
    USER_ACTIVATED_MESSAGE,
    USER_DEACTIVATED_MESSAGE,
    USER_NOT_FOUND_MESSAGE,
)
from app.core.dependencies import admin, get_current_user
from app.interface.user_interface import UserInterface
from app.models.user import User
from app.schema.auth_schema import FullUserResponse
from app.schema.response_schema import SuccessResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(admin)])


@router.get("", response_model=list[FullUserResponse], status_code=status.HTTP_200_OK)
async def get_all_user(
    user_service: UserInterface = Depends(UserService),
):
    users = user_service.get_all_users()
    return users


@router.get(
    "/{user_id}", response_model=FullUserResponse, status_code=status.HTTP_200_OK
)
async def get_user(
    user_id,
    user_service: UserInterface = Depends(UserService),
):
    user = user_service.get_user(user_id)
    return user


@router.put(
    "/{user_id}/activate",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
def activate_user(user_id: int, user_service: UserInterface = Depends(UserService)):
    if user_service.activate_user(user_id):
        return {"message": USER_ACTIVATED_MESSAGE}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND_MESSAGE
        )


@router.put(
    "/{user_id}/deactivate",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
def deactivate_user(user_id: int, user_service: UserInterface = Depends(UserService)):
    if user_service.deactivate_user(user_id):
        return {"message": USER_DEACTIVATED_MESSAGE}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND_MESSAGE
        )


@router.delete(
    "/{user_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK
)
def delete_user(
    user_id,
    current_user: User = Depends(get_current_user),
    user_service: UserInterface = Depends(UserService),
):
    user = user_service.delete_user(user_id, current_user)
    response = JSONResponse(user)
    return response
