from core.database import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp

from . import ModelBase

users_jobs = Table(
    "user_jobs",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), index=True),
    Column("job_id", ForeignKey("jobs.id"), index=True),
)


class User(Base, ModelBase):

    __tablename__ = "users"
    mysql_charset = ("utf8mb4",)
    mysql_collate = "utf8mb4_unicode_ci"

    full_name = Column(String(64))
    email = Column(String(200), unique=True, index=True, nullable=False)
    email_verified = Column(Boolean, nullable=False, server_default="0")
    hashed_password = Column(Text, nullable=False)
    scopes = Column(Text)

    updated_at = Column(
        DateTime,
        nullable=False,
        default=current_timestamp(),
        onupdate=func.utc_timestamp(),
    )
    jobs = relationship("Job", secondary=users_jobs, backref="users")

    def to_dict(self) -> dict:
        return self.__dict__.copy()
