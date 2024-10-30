from fastapi import APIRouter, Depends, status

from skylock.api import models
from skylock.api.dependencies import get_skylock_facade
from skylock.skylock_facade import SkylockFacade
from skylock.utils.security import get_current_user

router = APIRouter(tags=["Resource"], prefix="/folders")


@router.post(
    "/{path:path}",
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
    print(path)
    skylock.create_folder_for_user(path, user)
    return {"message": "Folder created"}


@router.delete(
    "/{path:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a folder",
    description=(
        "This endpoint allows the user to delete a specified folder. The folder must "
        "be empty to be deleted unless the 'recursive' parameter is set to True, "
        "which allows for recursive deletion. If the folder contains any files or "
        "subfolders and 'recursive' is not set, an error will be raised."
    ),
    responses={
        204: {
            "description": "Folder deleted successfully",
        },
        401: {
            "description": "Unauthorized user",
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
            },
        },
        403: {
            "description": "Deleting the root folder is forbidden",
            "content": {
                "application/json": {
                    "example": {"detail": "Deleting your root folder is forbidden"}
                }
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
            "description": "Folder not empty",
            "content": {
                "application/json": {"example": {"detail": "Folder not empty"}}
            },
        },
    },
)
def delete_folder(
    path: str,
    recursive: bool = False,
    user: models.User = Depends(get_current_user),
    skylock: SkylockFacade = Depends(get_skylock_facade),
):
    skylock.delete_folder(path=path, user=user, is_recursively=recursive)
    return {"message": "Folder deleted"}
