from core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp

from . import ModelBase


class Category(Base, ModelBase):

    __tablename__ = "categories"
    mysql_charset = ("utf8mb4",)
    mysql_collate = "utf8mb4_unicode_ci"

    name = Column(String(64))
    parent_category_id = Column(String(32), ForeignKey("categories.id"), index=True, nullable=True)

    updated_at = Column(
        DateTime,
        nullable=False,
        default=current_timestamp(),
        onupdate=func.utc_timestamp(),
    )

    # Categoryテーブル自身へのリレーションを定義
    parent_category = relationship(
        "Category",
        foreign_keys=[parent_category_id],
        remote_side="[Category.id]",
        back_populates="children_category",
        uselist=False,
    )  # type: ignore
    children_category = relationship("Category", back_populates="parent_category")  # type: ignore

    def to_dict(self) -> dict:
        return self.__dict__.copy()
