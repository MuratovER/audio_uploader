from typing import Annotated

from fastapi import APIRouter, Depends

from services.oauth import get_current_user

router = APIRouter(prefix="/user", tags=["User"])


@router.get(
    path="/current",
)
async def get_current_user_info(
    current_user: Annotated[int, Depends(get_current_user)],
):
    return current_user
