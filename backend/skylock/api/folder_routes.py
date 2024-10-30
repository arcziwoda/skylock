from fastapi import APIRouter, Depends, status

from skylock.api import models
from skylock.api.dependencies import get_skylock_facade
from skylock.skylock_facade import SkylockFacade
from skylock.utils.security import get_current_user

router = APIRouter(tags=["Resource"], prefix="/folders")


@router.post(
    "{path:path}",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new folder",
    description="This endpoint allows the user to create a new folder at the specified path. If the folder already exists or the path is invalid, appropriate errors will be raised.",
    responses={
        201: {
            "description": "Folder created successfully",
            "content": {"application/json": {"example": {"message": "Folder created"}}},
        },
        400: {
            "description": "Invalid path provided",
            "content": {"application/json": {"example": {"detail": "Invalid path"}}},
        },
        401: {
            "description": "Unauthorized user",
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
            },
        },
        404: {
            "description": "Resource not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Resource not found",
                        "missing": "folder_name",
                    }
                }
            },
        },
        409: {
            "description": "Resource already exists",
            "content": {
                "application/json": {"example": {"detail": "Resource already exists"}}
            },
        },
    },
)
def create_folder(
    path: str,
    user: models.User = Depends(get_current_user),
    skylock: SkylockFacade = Depends(get_skylock_facade),
):
    skylock.create_folder_for_user(path, user)
    return {"message": "Folder created"}
