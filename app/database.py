from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, VARCHAR, create_engine

from config import setup_config, Config


class Application:
    config: Optional[Config] = None
    # database: Optional[Database] = None


app = Application()


# создаем базовый класс для моделей
# создаем модель, объекты которой будут храниться в бд
class Base(DeclarativeBase):
    pass


class ParseDataModel(Base):
    __tablename__ = "_fds321"
    id = Column(Integer, index=True, primary_key=True)
    added_at = Column(VARCHAR(255))
    url = Column(VARCHAR(255))
    stars = Column(VARCHAR(255))
    fork = Column(VARCHAR(255))
    last_commit = Column(VARCHAR(255))
    last_release = Column(VARCHAR(255))


def create_db(engine):
    # создаем таблицы
    Base.metadata.create_all(bind=engine)


def run_engine():
    setup_config(app)

    # # for postgresql
    # db_url = f'postgresql+psycopg2://{app.config.database.user}:{app.config.database.password}@' \
    #          f'{app.config.database.host}:{app.config.database.port}/{app.config.database.database}'

    # for mysql
    db_url = f'mysql+mysqlconnector://{app.config.database.user}:{app.config.database.password}@' \
             f'{app.config.database.host}:{app.config.database.port}/{app.config.database.database}'
    print(db_url)
    app.engine = create_engine(db_url)
    create_db(app.engine)
