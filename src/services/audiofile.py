import os
from pathlib import Path
from typing import Optional

from fastapi import Depends, UploadFile
from loguru import logger
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.config import settings
from core.constants import get_available_audio_types
from core.exceptions import (
    filename_arleady_exist_exception,
    filename_was_not_provided,
    max_file_size_exception,
    unsuported_audio_type_provided,
)
from db.models.audio import AudioFile
from db.repositories.audiofile import AudioFileRepository
from db.session import get_session


class AudioFilesService:
    def __init__(
        self,
        repository: AudioFileRepository = Depends(),
        session: AsyncSession = Depends(get_session),
    ) -> None:
        self._repository = repository
        self._session = session

    @staticmethod
    def get_file_size(file: UploadFile) -> float:
        """
        Get file size in Mb.
        """

        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        return size / (1024 * 1024)

    async def upload_file(
        self, audiofile: UploadFile, filename: Optional[str], user_id: int
    ) -> AudioFile:
        """
        Receive File & store to disk.
        """
        if (
            filesize := self.get_file_size(file=audiofile)
        ) > settings().MAX_FILE_SIZE_IN_MB:
            logger.error(f"File size: {filesize}")
            raise max_file_size_exception

        if audiofile.content_type not in get_available_audio_types():
            logger.error(f"File type: {audiofile.content_type}")
            raise unsuported_audio_type_provided

        if not audiofile.filename:
            raise filename_was_not_provided

        if filename and await self._repository.file_exist(
            user_id=user_id, filename=filename
        ):
            logger.error(f"File #{filename} for user {user_id} exists.")
            raise filename_arleady_exist_exception

        if filename:
            extension = audiofile.filename.split(".")[-1]
            filename = filename + "." + extension
        else:
            filename = audiofile.filename

        audiofile_from_db = await self._repository.create(
            user_id=user_id, filename=filename
        )

        tmp_file_dir = f"../files/{user_id}"

        Path(tmp_file_dir).mkdir(parents=True, exist_ok=True)

        with open(os.path.join(tmp_file_dir, filename), "wb") as disk_file:
            file_bytes = await audiofile.read()
            disk_file.write(file_bytes)

        await self._session.commit()

        return audiofile_from_db
