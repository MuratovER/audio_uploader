from schemas.base import BaseOrmSchema


class AuthSchema(BaseOrmSchema):
    access_token: str
    expires_in: int
    refresh_token: str
    token_type: str
