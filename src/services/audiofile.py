import os
from pathlib import Path

from fastapi import Depends, UploadFile
from loguru import logger
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.constants import get_available_audio_types
from core.exceptions import (
    filename_arleady_exist_exception,
    filename_was_not_provided,
    unsuported_audio_type_provided,
)
from db.repositories.audiofile import AudioFileRepository
from db.session import get_session
from schemas.audiofile import AudioFileSchema


class AudioFilesService:
    def __init__(
        self,
        repository: AudioFileRepository = Depends(),
        session: AsyncSession = Depends(get_session),
    ) -> None:
        self._repository = repository
        self._session = session

    async def upload_file(self, audiofile: UploadFile, audiofile_data: AudioFileSchema):
        """
        Receive File, store to disk
        """

        if audiofile.content_type not in get_available_audio_types():
            logger.error(f"File type: {audiofile.content_type}")
            raise unsuported_audio_type_provided

        if not audiofile.filename:
            raise filename_was_not_provided

        if audiofile_data.filename and await self._repository.file_exist(
            user_id=audiofile_data.user_id, filename=audiofile_data.filename
        ):
            logger.error(
                f"File #{audiofile_data.filename} for user {audiofile_data.user_id} exists."
            )
            raise filename_arleady_exist_exception

        if audiofile_data.filename:
            extension = audiofile.filename.split(".")[-1]
            filename = audiofile_data.filename + "." + extension
        else:
            filename = audiofile.filename

        audiofile_from_db = await self._repository.create(
            user_id=audiofile_data.user_id, filename=filename
        )

        tmp_file_dir = f"../files/{audiofile_data.user_id}"

        Path(tmp_file_dir).mkdir(parents=True, exist_ok=True)

        with open(os.path.join(tmp_file_dir, filename), "wb") as disk_file:
            file_bytes = await audiofile.read()
            disk_file.write(file_bytes)

        await self._session.commit()

        return audiofile_from_db
