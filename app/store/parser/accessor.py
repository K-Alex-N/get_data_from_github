from flask_login import current_user
from sqlalchemy import select

from app.store.db import session, try_except_session
from app.store.db.models import PullRequest, Url, ParseData


def create_pull_request(name, links):
    pull_request = PullRequest(name=name, user_id=current_user.id)
    with try_except_session() as session:
        session.add(pull_request)
        session.flush()

        for link in links:
            url = Url(pull_request_id=pull_request.id, url=link)
            session.add(url)

    return pull_request.id


def create_dict_by_pull_request_id(pull_request_id):
    d = {}
    urls_id = session.scalars(select(Url).where(Url.pull_request_id == pull_request_id)).all()
    for u in urls_id:
        d[u.id] = {}
        data_by_url_id = session.scalars(select(ParseData).where(ParseData.url_id == u.id)).all()
        for data in data_by_url_id:
            d[u.id][str(data.added_at)] = {
                'stars': data.stars,
                'fork': data.fork,
                'last_commit': data.last_commit,
                'last_release': data.last_release}
    return d
