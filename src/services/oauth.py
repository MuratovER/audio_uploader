from typing import Annotated, Any, Literal

import requests
from fastapi import Depends
from fastapi.security import APIKeyHeader

from core.config import settings
from core.exceptions import invalid_access_token_exception, yandex_oauth_exception
from schemas.auth import AuthSchema

header_scheme = APIKeyHeader(name="Authorization")


class YaOauthService:
    async def request(
        self, request_type: Literal["login"] | Literal["refresh"], token: str
    ) -> AuthSchema:
        url = "https://oauth.yandex.ru/token"
        data = {
            "client_id": settings().YA_CLIENT_ID,
            "client_secret": settings().YA_SECRET,
        }

        match request_type:
            case "login":
                data["grant_type"] = "authorization_code"
                data["code"] = token

            case "refresh":
                data["grant_type"] = "refresh_token"
                data["refresh_token"] = token

        response = requests.post(url=url, data=data)

        if response.status_code != 200:
            yandex_oauth_exception.detail += response.json().get("error_description")
            raise yandex_oauth_exception

        return AuthSchema(**response.json())


async def get_current_user(
    token: Annotated[str, Depends(header_scheme)],
) -> dict[str, Any]:
    login_data = {"oauth_token": token, "format": "json"}
    response = requests.post("https://login.yandex.ru/info", data=login_data)

    if response.status_code != 200:
        raise invalid_access_token_exception

    return response.json()
