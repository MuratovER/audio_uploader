from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, UploadFile

from db.models.audio import AudioFile
from schemas.audiofile import AudioFileSchema
from services.audiofile import AudioFilesService
from services.oauth import get_current_user

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
    current_user_id: Annotated[int, Depends(get_current_user)],
    audiofile_service: AudioFilesService = Depends(),
    filename: Optional[str] = Query(None, max_length=255),
) -> AudioFile:
    return await audiofile_service.upload_file(
        audiofile=audiofile, filename=filename, user_id=current_user_id
    )
