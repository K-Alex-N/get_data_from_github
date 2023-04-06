import os
from flask import Flask
def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


def run_app():
    app = create_app()
    app.run()

    @app.route('/')
    def hello():
        return 'Hello, World!'

    # run_db()
