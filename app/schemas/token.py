from typing import Optional

from schemas.core import BaseSchema


class Token(BaseSchema):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True
        alias_generator = None
        allow_population_by_field_name = False


class TokenPayload(BaseSchema):
    sub: Optional[str]
