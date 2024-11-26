from typing import Annotated

from fastapi import APIRouter, Depends, Response

from skylock.api import models
from skylock.api.dependencies import get_skylock_facade
from skylock.skylock_facade import SkylockFacade

router = APIRouter(tags=["Resource"], prefix="/shared")


@router.get(
    "/folders/{folder_id}",
    summary="Get public folder contents",
    description=(
        """
        This endpoint retrieves the contents of a shared folder.
        It returns a list of files and subfolders contained within the folder at the provided path.
        If path is empty, no contents will be shown.
        """
    ),
    responses={
        200: {
            "description": "Successful retrieval of shared folder contents",
            "content": {
                "application/json": {
                    "example": {
                        "files": [
                            {"name": "file1.txt", "path": "/folder/file1.txt"},
                            {"name": "file2.txt", "path": "/folder/file2.txt"},
                        ],
                        "folders": [
                            {"name": "subfolder1", "path": "/folder/subfolder1"},
                            {"name": "subfolder2", "path": "/folder/subfolder2"},
                        ],
                    }
                }
            },
        },
        401: {
            "description": "Unauthorized user",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
        },
        404: {
            "description": "Folder not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Resource not found",
                        "missing": "folder_name",
                    }
                }
            },
        },
    },
)
def get_public_folder_contents(
    folder_id: str,
    skylock: Annotated[SkylockFacade, Depends(get_skylock_facade)],
) -> models.FolderContents:
    return skylock.get_public_folder_contents(folder_id)


@router.get(
    "/files/download/{file_id}",
    summary="Download a public file",
    description="This endpoint allows users to download a shared (public) file by id.",
    responses={
        200: {
            "description": "File downloaded successfully",
            "content": {"application/octet-stream": {}},
        },
        400: {
            "description": "Invalid file id provided, most likely not shared",
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
def download_public_file(
    file_id: str,
    skylock: Annotated[SkylockFacade, Depends(get_skylock_facade)],
):
    file_data = skylock.download_public_file(file_id)
    return Response(content=file_data.read(), media_type="application/octet-stream")
