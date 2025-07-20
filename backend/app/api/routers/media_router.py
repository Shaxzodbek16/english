from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException

from app.api.schemas import MediaSchemaResponse, MediaClearSchema
from app.api.controllers import MediaController
from app.api.utils.jwt_handler import get_current_user

router = APIRouter(
    prefix="/media",
    tags=["Media Management"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "/upload/",
    status_code=status.HTTP_201_CREATED,
    response_model=MediaSchemaResponse,
    summary="Upload media file",
    description="Upload a media file (image, video, audio, etc.) to the server.",
)
async def upload(
    static: bool = False,
    file: UploadFile = File(...),
    media_controller: MediaController = Depends(),
):
    return await media_controller.upload(file, static=static)


@router.delete(
    "/clear/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete media file",
    description="Delete a media file from the server.",
)
async def clear(
    file_path: MediaClearSchema,
    media_controller: MediaController = Depends(),
):
    try:
        media_controller.clear(file_path.media_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete file: {e}",
        )
    return {"detail": "File deleted successfully"}
