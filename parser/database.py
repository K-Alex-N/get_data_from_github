import datetime
import os
from dataclasses import dataclass
from typing import Optional, Union
import psycopg2
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import Column, Integer, VARCHAR, create_engine

from config import setup_config


def run_engine(app, config_path):
    dbc = setup_config(config_path)
    print(dbc)
    # db_url = f'postgresql+psycopg2://{dbc.user}:{dbc.password}@{dbc.host}:{dbc.port}/{dbc.database}')
    # return create_engine(potgres_database, echo=False)



engine = 1

# создаем базовый класс для моделей
class Base(DeclarativeBase): pass


# создаем модель, объекты которой будут храниться в бд
class ParseDataModel(Base):
    __tablename__ = "_fds321"
    id = Column(Integer, index=True, primary_key=True)
    added_at = Column(VARCHAR(255))
    url = Column(VARCHAR(255))
    stars = Column(VARCHAR(255))
    fork = Column(VARCHAR(255))
    last_commit = Column(VARCHAR(255))
    last_release = Column(VARCHAR(255))

    # # кусок пода из KTS обучалки. зачем он?
    # def to_dataclass(self) -> ParseData:
    #     pd = ParseData( id = self.id,
    #                     added_at = self.added_at,
    #                     url = self.url,
    #                     stars = self.stars,
    #                     fork = self.fork,
    #                     last_commit = self.last_commit,
    #                     last_release = self.last_release)
    #     return pd


# создаем таблицы
Base.metadata.create_all(bind=engine)


def add_data_sqlalchemy(url, stars, fork, last_commit, last_release):
    with Session(bind=engine) as db:
        x = ParseDataModel(added_at=datetime.datetime.now(),
                           url=url,
                           stars=stars,
                           fork=fork,
                           last_commit=last_commit,
                           last_release=last_release)
        db.add(x)
        db.commit()


def get_data_sqlalchemy():
    with Session(bind=engine) as db:
        data = db.query(ParseDataModel).all()
        for x in data:
            f = f'{x.url} {x.fork} {x.stars}'
            print(f)


# def add_data_row_sql(url, stars, fork, last_commit, last_release):
#     connection = psycopg2.connect(
#         host="localhost",
#         database="kts",
#         user="kts_user",
#         password="kts_pass")
#
#     connection.autocommit = True
#
#     user = '_fds'
#     kit = 321
#     db_name = user + str(kit)
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f'CREATE TABLE IF NOT EXISTS {db_name} (' + """
#             id serial PRIMARY KEY,
#             added_at time,
#             url text,
#             stars text,
#             fork text,
#             last_commit timestamptz ,
#             last_release text) """
#         )
#
#         # в чем разнича между time и timestamptz?
#
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f'INSERT INTO _fds321 (added_at, url, stars, fork, last_commit, last_release) VALUES'
#             f'(Current_time, \'{url}\', {stars}, {fork}, \'{last_commit}\', \'{last_release}\');'
#         )
#
#     # создается для каждого пользователя отдельная БД видимо НЕ РЕЛЯЦИОННАЯ.
#     # просто записывать JSON данные для разных сайтов
#     # затем по url выдергивать все JSON и составлять из них таблицу
