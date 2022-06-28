import datetime
from typing import Any, List, Optional

from pydantic import root_validator
from schemas.core import BaseSchema, PagingMeta


class JobResponse(BaseSchema):
    id: str
    title: Optional[str]
    hashtags: Optional[List[str]]
    deleted_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class JobCreate(BaseSchema):
    title: str
    description: Optional[str]
    data_type: Optional[int] = 0
    _VALIDATION_REQUIRED_CONFIGS: dict[str, Any] = {"data_type": {"case": 1, "required_fields": ["description"]}}

    @root_validator
    def validate_description(cls, values):
        for key, config in cls._VALIDATION_REQUIRED_CONFIGS.items():
            if values.get(key) != config.get("case"):
                continue
            for field in config.get("required_fields"):
                if not values.get(field):
                    raise ValueError(f"{field} required if {key}={config.get('case')}.")
        values.pop("data_type")
        return values


class JobUpdate(BaseSchema):
    title: Optional[str] = None


class JobsPagedResponse(BaseSchema):
    data: Optional[List[JobResponse]]
    meta: Optional[PagingMeta]
