import os

from parser.database import get_data_sqlalchemy, run_engine
from parser.parcer import repeat, parce_urls

class Application:
    pass

app = Application()


if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.yml")
    run_engine(app, config_path)

    urls = [
        'https://github.com/django/django',
        'https://github.com/pallets/flask',
        'https://github.com/tiangolo/fastapi',
        'https://github.com/tornadoweb/tornado',
        'https://github.com/aio-libs/aiohttp',
        'https://github.com/sanic-org/sanic',
        'https://github.com/bottlepy/bottle',
        'https://github.com/Pylons/pyramid',
        'https://github.com/cherrypy/cherrypy',
    ]

    # SERVER_MODE = False
    # if not SERVER_MODE:
    #     get_html = False
    #     save_data = True
    #     is_repeat_active = False
    #     get_data = False
    #
    #     if is_repeat_active:
    #         days = 1
    #         at = '8:50'
    #         repeat(days, at, urls)
    #     else:
    #         parce_urls(urls)
    #
    #     if get_data:
    #         get_data_sqlalchemy()
    # else:
    #     days = 1
    #     at = '2:00'
    #     repeat(days, at, urls)
