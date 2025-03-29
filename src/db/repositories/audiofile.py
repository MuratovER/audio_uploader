from sqlalchemy import select

from db.models.audio import AudioFile
from db.repositories.base import BaseDatabaseRepository


class AudioFileRepository(BaseDatabaseRepository):
    async def file_exist(self, user_id: int, filename: str) -> bool:
        query_result = await self._session.execute(
            select(AudioFile).where(
                AudioFile.user_id == user_id, AudioFile.filename == filename
            )
        )
        return bool(query_result.scalars().all())

    async def create(self, user_id: int, filename: str) -> AudioFile:
        audiofile = AudioFile(user_id=user_id, filename=filename)  # type: ignore
        self._session.add(audiofile)
        await self._session.flush()

        return audiofile
