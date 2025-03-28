from fastapi import APIRouter, Depends, UploadFile

from core.checkers import post_create_data_checker
from db.models.audio import AudioFile
from schemas.audiofile import AudioFileSchema
from services.audiofile import AudioFilesService

router = APIRouter(prefix="/audios", tags=["Audio files"])


@router.post(
    path="/",
    response_model=AudioFileSchema,
)
async def post_media_file(
    audiofile: UploadFile,
    data: AudioFileSchema = Depends(post_create_data_checker),
    audiofile_service: AudioFilesService = Depends(),
) -> AudioFile:
    return await audiofile_service.upload_file(audiofile=audiofile, audiofile_data=data)
