from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.store.db import Base


class User(Base, UserMixin):
    __tablename__ = "user"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    username:           Mapped[str]
    password:           Mapped[str]
    email:              Mapped[str]     # may be put as Optional ?
    is_email_confirmed: Mapped[bool] = False

    # pill_requests = db.relationship('PullRequest')

class PullRequest(Base):
    __tablename__ = "pull_request"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    name:               Mapped[str]
    user_id =           mapped_column(ForeignKey("user.id"))   # may we put here "User.id" ?
    start_date:         Mapped[datetime] = mapped_column(insert_default=func.now())

class Url(Base):
    __tablename__ = "url"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    pull_request_id =   mapped_column(ForeignKey("pull_request.id"))   # may we put here "PullRequest.id" ?
    url:                Mapped[str]

class ParseData(Base):
    __tablename__ = "parse_data"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    url_id =            mapped_column(ForeignKey("url.id"))           # Url.id
    added_at:           Mapped[datetime] = mapped_column(insert_default=func.now())
    stars:              Mapped[str]
    fork:               Mapped[str]
    last_commit:        Mapped[str]
    last_release:       Mapped[str]


