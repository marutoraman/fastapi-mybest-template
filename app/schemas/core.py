from typing import Any, Optional

from fastapi import Query
from humps import camel
from pydantic import BaseModel, validator


def to_camel(string: str) -> str:
    return camel.case(string)


class BaseSchema(BaseModel):

    # @validator("*", pre=True)
    # def cast_someone(cls, v):
    #     '''
    #     全ての項目に対して、pre処理を行いたい場合の例
    #     '''
    #     if isinstance(v, Any):
    #         return v
    #     return v

    # @validator("*", pre=True)
    # def split_comma(cls, v):
    #     '''
    #     カンマでsplitする例
    #     '''
    #     if isinstance(v, str):
    #         return v.split(",")
    #     return v

    class Config:
        """
        # キャメルケース　<-> スネークケースの自動変換
        pythonではスネークケースを使用するが、Javascriptではキャメルケースを使用する場合が多いため
        変換する必要がある
        """

        alias_generator = to_camel
        allow_population_by_field_name = True


class PagingMeta(BaseSchema):
    current_page: int
    total_page_count: int
    total_data_count: int


class PagingQueryIn(BaseSchema):
    page: int = Query(1)
    per_page: int = Query(30)

    @validator("page")
    def validate_page(cls, v: int) -> int:
        return 1 if not v >= 1 else v

    @validator("per_page")
    def validate_per_page(cls, v: int) -> int:
        return 30 if not v >= 1 else v

    def get_offset(self) -> int:
        return (self.page - 1) * self.per_page if self.page >= 1 and self.per_page >= 1 else 0

    def set_paging_query(self, query: Any) -> Any:
        offset = self.get_offset()
        return query.offset(offset).limit(self.per_page)


class FilterQueryIn(BaseSchema):
    sort: str = Query(None)
    direction: str = Query(None)
    start: Optional[int] = Query(None)
    end: Optional[int] = Query(None)

    @validator("direction")
    def validate_direction(cls, v: str) -> str:
        if not v:
            return "asc"
        if v not in ["asc", "desc"]:
            raise ValueError("asc or desc only")
        return v

    def validate_allowed_sort_column(self, allowed_columns: list) -> bool:
        if not self.sort:
            return True
        return self.sort in allowed_columns
