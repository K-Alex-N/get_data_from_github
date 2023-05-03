from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass

from app.store.db.models import *

engine = create_engine("postgresql+psycopg2://kts_user:kts_pass@localhost:5432/flask", echo=False)
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

@contextmanager
def try_except_session():
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

