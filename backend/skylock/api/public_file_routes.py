from typing import Annotated

from fastapi import Depends, Response

from skylock.api.dependencies import get_skylock_facade
from skylock.skylock_facade import SkylockFacade
from skylock.api.public_folder_routes import router


@router.get(
    "/files/{file_id:path}",
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
