from typing import Optional

from schemas.base import BaseOrmSchema


class AudioFileSchema(BaseOrmSchema):
    user_id: str
    filename: Optional[str] = None
