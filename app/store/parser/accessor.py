from flask import flash
from flask_login import current_user
from sqlalchemy import select

from app.store.db import session, try_except_session
from app.store.db.models import PullRequest, Url, ParseData


def create_new_parser(name, links):
    pull_request = PullRequest(name=name, user_id=current_user.id)
    with try_except_session() as session:
        session.add(pull_request)
        session.flush()

        for link in links:
            url = Url(pull_request_id=pull_request.id, url=link)
            session.add(url)

    return pull_request.id


def change_parser(name, new_links_str: set[str], pull_request_id:int):
    with try_except_session() as session:
        pull_request = session.scalar(select(PullRequest).where(PullRequest.id == pull_request_id))
        # change name
        if pull_request.name != name:
            pull_request.name = name
        # change links
        cur_links_odj = session.scalars(select(Url).where(Url.pull_request_id == pull_request.id)).all()
        # все старое (то что не повторилось в new_links) удаляем
        for link in cur_links_odj:
            if link.url in new_links_str:
                new_links_str.remove(link.url)
            else:
                session.delete(link)
        # все оставщееся из new_links добавляем
        for link in new_links_str:
            session.add(
                Url(
                    pull_request_id=pull_request_id,
                    url=link)
            )

    return pull_request_id


def create_dict_by_pull_request_id(pull_request_id):
    d = {}
    urls_id = session.scalars(select(Url).where(Url.pull_request_id == pull_request_id)).all()
    for u in urls_id:
        d[u.url] = {}
        data_by_url_id = session.scalars(select(ParseData).where(ParseData.url_id == u.id)).all()
        for data in data_by_url_id:
            d[u.url][str(data.added_at.date())] = {
                'stars': data.stars,
                'fork': data.fork,
                'last_commit': data.last_commit,
                'last_release': data.last_release}
    return d
