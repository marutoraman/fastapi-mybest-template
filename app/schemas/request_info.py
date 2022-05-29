import datetime
from typing import List, Optional

from schemas.core import BaseSchema, PagingMeta


class RequestInfoResponse(BaseSchema):
    ip_address: Optional[str]
    host: Optional[str]

    class Config:
        orm_mode = True


