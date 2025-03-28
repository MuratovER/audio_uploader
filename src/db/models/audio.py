from sqlalchemy import PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import BaseModel


class AudioFile(BaseModel):
    user_id: Mapped[str] = mapped_column(
        String(length=255), primary_key=True, nullable=False
    )
    filename: Mapped[str] = mapped_column(
        String(length=255), primary_key=True, nullable=False
    )

    __table_args__ = (PrimaryKeyConstraint("user_id", "filename"),)

    def __str__(self) -> str:
        return f"AudioFile #{self.filename} of user #{self.user_id}"
