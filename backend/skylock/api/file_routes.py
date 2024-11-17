from typing import Annotated

from fastapi import APIRouter, Depends, Response, UploadFile, status

from skylock.api.dependencies import get_current_user, get_skylock_facade
from skylock.api.validation import validate_path_not_empty
from skylock.database import models as db_models
from skylock.skylock_facade import SkylockFacade
from skylock.utils.path import UserPath

router = APIRouter(tags=["Resource"], prefix="/files")


@router.post(
    "/upload/{path:path}",
    summary="Upload a file",
    description=(
        """
        This endpoint allows users to upload a file to a specified path.
        If the file already exists, an appropriate error will be raised.
        """
    ),
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "File uploaded successfully",
            "content": {"application/json": {"example": {"message": "File uploaded successfully"}}},
        },
        400: {
            "description": "Invalid path provided, most likely empty",
            "content": {"application/json": {"example": {"detail": "Invalid path"}}},
        },
        401: {
            "description": "Unauthorized user",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
        },
        409: {
            "description": "Resource already exists",
            "content": {"application/json": {"example": {"detail": "File already exists"}}},
        },
    },
)
def upload_file(
    file: UploadFile,
    path: Annotated[str, Depends(validate_path_not_empty)],
    user: Annotated[db_models.UserEntity, Depends(get_current_user)],
    skylock: Annotated[SkylockFacade, Depends(get_skylock_facade)],
):
    skylock.upload_file(user_path=UserPath(path=path, owner=user), file_data=file.file)


@router.get(
    "/download/{path:path}",
    summary="Download a file",
    description="This endpoint allows users to download a file from a specified path.",
    responses={
        200: {
            "description": "File downloaded successfully",
            "content": {"application/octet-stream": {}},
        },
        400: {
            "description": "Invalid path provided, most likely empty",
            "content": {"application/json": {"example": {"detail": "Invalid path"}}},
        },
        401: {
            "description": "Unauthorized user",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
        },
        404: {
            "description": "File not found",
            "content": {"application/json": {"example": {"detail": "File not found"}}},
        },
    },
)
def download_file(
    path: Annotated[str, Depends(validate_path_not_empty)],
    user: Annotated[db_models.UserEntity, Depends(get_current_user)],
    skylock: Annotated[SkylockFacade, Depends(get_skylock_facade)],
):
    file_data = skylock.download_file(UserPath(path=path, owner=user))
    return Response(content=file_data.read(), media_type="application/octet-stream")
