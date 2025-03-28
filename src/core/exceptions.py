from fastapi import HTTPException, status

not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found.",
)

filename_arleady_exist_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Filename arleady exist.",
)

filename_was_not_provided = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Filename was not provided.",
)

unsuported_audio_type_provided = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Unsuported audio type provided.",
)
