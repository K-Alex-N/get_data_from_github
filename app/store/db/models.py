from datetime import datetime
from typing import List, Optional

from flask_login import UserMixin
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.store.db import Base


class User(Base, UserMixin):
    __tablename__ = "user"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    username:           Mapped[str]
    password:           Mapped[str]
    email:              Mapped[str]
    is_email_confirmed: Mapped[bool] = mapped_column(default=False)

    pull_requests:      Mapped[List['PullRequest']] = relationship(back_populates='user', cascade="all, delete-orphan")

class PullRequest(Base):
    __tablename__ = "pull_request"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    name:               Mapped[str]
    user_id =           mapped_column(ForeignKey("user.id"))
    start_date:         Mapped[datetime] = mapped_column(insert_default=func.now())

    user:               Mapped['User'] = relationship(back_populates='pull_requests')
    urls:               Mapped[List['Url']] = relationship(back_populates='pull_request', cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"PullRequest(id={self.id!r}, name={self.name!r}, user_id={self.user_id!r} etc...)"

class Url(Base):
    __tablename__ = "url"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    pull_request_id =   mapped_column(ForeignKey("pull_request.id"))
    url:                Mapped[str]

    pull_request:       Mapped['PullRequest'] = relationship(back_populates='urls')
    parse_data:         Mapped[List['ParseData']] = relationship(back_populates='url', cascade="all, delete-orphan")

class ParseData(Base):
    __tablename__ = "parse_data"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    url_id =            mapped_column(ForeignKey("url.id"))
    added_at:           Mapped[datetime] = mapped_column(insert_default=func.now())
    stars:              Mapped[str]
    fork:               Mapped[str]
    last_commit:        Mapped[str]
    last_release:       Mapped[Optional[str]]

    url:                Mapped['Url'] = relationship(back_populates='parse_data')

"""
DROP TABLE parse_data;
DROP TABLE url;
DROP TABLE pull_request;
DROP TABLE "user";
"""
