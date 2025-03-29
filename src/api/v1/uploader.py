from collections.abc import Sequence
from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, Query, UploadFile

from db.models.audio import AudioFile
from schemas.audiofile import AudioFileSchema
from services.audiofile import AudioFilesService
from services.oauth import get_admin_user, get_current_user

router = APIRouter(prefix="/audios", tags=["Audio files"])


@router.post(
    path="/",
    response_model=AudioFileSchema,
    description=(
        "If filename was not setted, name of the file will be used.\n\n"
        "Max file size 1MB."
    ),
)
async def post_media_file(
    audiofile: UploadFile,
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
    audiofile_service: AudioFilesService = Depends(),
    filename: Optional[str] = Query(None, max_length=255),
) -> AudioFile:
    return await audiofile_service.upload_file(
        audiofile=audiofile, filename=filename, user_id=int(current_user["id"])
    )


@router.get(
    path="/{user_id: int}",
    response_model=list[AudioFileSchema],
)
async def get_files_by_user_id(
    user_id: int,
    current_user_id: Annotated[int, Depends(get_admin_user)],
    audiofile_service: AudioFilesService = Depends(),
) -> Sequence[AudioFile]:
    return await audiofile_service.get_files_by_user_id(user_id=user_id)
