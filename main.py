from parser.accessor import get_data_sqlalchemy
from parser.parcer import repeat, parce_urls

if __name__ == '__main__':

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

    # # SERVER_MODE:
    # days = 1
    # at = '2:00'
    # repeat(days, at, urls)
    #
    # # TESTS
    # # if repeat
    # days = 1
    # at = '8:50'
    # repeat(days, at, urls)

    # if start parce data
    parce_urls(urls)




