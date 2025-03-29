from typing import Optional

from pydantic import Field

from schemas.base import BaseOrmSchema


class AudioFileSchema(BaseOrmSchema):
    user_id: int
    filename: str


class UploadAudioSchema(BaseOrmSchema):
    filename: Optional[str] = Field(None, max_length=255)
