from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import config


class Base(DeclarativeBase):
    pass


from app.store.db.models import *

db_url = f"postgresql+psycopg2://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"
engine = create_engine(db_url)
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()


@contextmanager
def try_except_session():
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
