import schedule

from app.models import Url
from app.parser import parse_urls


def every_day_parsing():
    urls = Url.query.all()
    if not parse_urls(urls):
        pass
        # отправлять алерт на почту

def run_cycle():
    schedule.every().day.at('21:00').do(every_day_parsing)
    while True:
        schedule.run_pending()