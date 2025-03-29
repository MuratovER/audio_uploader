import webbrowser
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from core.config import settings
from schemas.auth import AuthSchema
from services.oauth import YaOauthService, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    path="/login",
    response_model=AuthSchema,
)
async def login(
    code: str,
    auth_service: YaOauthService = Depends(),
) -> AuthSchema:
    return await auth_service.request(request_type="login", token=code)


@router.post(
    path="/refresh",
    response_model=AuthSchema,
)
async def refresh(
    refresh_token: str,
    auth_service: YaOauthService = Depends(),
) -> AuthSchema:
    return await auth_service.request(request_type="refresh", token=refresh_token)


@router.get(
    path="/code",
)
async def get_code():
    webbrowser.open_new_tab(
        url=f"https://oauth.yandex.ru/authorize?response_type=code&client_id={settings().YA_CLIENT_ID}"
    )
    return HTTP_200_OK


@router.get(
    path="/user",
)
async def get_current_user_info(
    current_user: Annotated[int, Depends(get_current_user)],
):
    return current_user
