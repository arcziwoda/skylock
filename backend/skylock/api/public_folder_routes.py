from typing import Annotated

from fastapi import APIRouter, Depends

from skylock.api import models
from skylock.api.dependencies import get_skylock_facade
from skylock.skylock_facade import SkylockFacade

router = APIRouter(tags=["Resource"], prefix="/shared")


@router.get(
    "/folders/{folder_id:path}",
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
