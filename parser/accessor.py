from datetime import datetime
from sqlalchemy.orm import Session

from parser.database import app, ParseDataModel


def add_data_sqlalchemy(url, stars, fork, last_commit, last_release):
    with Session(bind=app.engine) as db:
        x = ParseDataModel(added_at=datetime.now(),
                           url=url,
                           stars=stars,
                           fork=fork,
                           last_commit=last_commit,
                           last_release=last_release)
        db.add(x)
        db.commit()


def get_data_sqlalchemy():
    with Session(bind=app.engine) as db:
        data = db.query(ParseDataModel).all()
        for x in data:
            f = f'{x.url} {x.fork} {x.stars}'
            print(f)
