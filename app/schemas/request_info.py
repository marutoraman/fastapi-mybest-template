from typing import Optional

from schemas.core import BaseSchema


class RequestInfoResponse(BaseSchema):
    ip_address: Optional[str]
    host: Optional[str]

    class Config:
        orm_mode = True
