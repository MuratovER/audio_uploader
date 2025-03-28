from fastapi import Form, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from schemas.audiofile import AudioFileSchema


def post_create_data_checker(data: str = Form(...)) -> AudioFileSchema:
    try:
        return AudioFileSchema.model_validate_json(data)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
