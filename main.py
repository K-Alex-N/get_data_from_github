import schedule
from flask import Flask, render_template

from app.parcer import parce_urls

if __name__ == '__main__':

    # urls = [
    #     'https://github.com/django/django',
    #     'https://github.com/pallets/flask',
    #     'https://github.com/tiangolo/fastapi',
    #     'https://github.com/tornadoweb/tornado',
    #     'https://github.com/aio-libs/aiohttp',
    #     'https://github.com/sanic-org/sanic',
    #     'https://github.com/bottlepy/bottle',
    #     'https://github.com/Pylons/pyramid',
    #     'https://github.com/cherrypy/cherrypy',
    # ]

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html', title='Парсер GitHub')

    app.run()
    # def repeat():
    #     parce_urls(urls)
    #
    # schedule.every().day.at('14:54').do(repeat)
    # while True:
    #     schedule.run_pending()





