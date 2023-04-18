from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='sfsdfw234sd23rwd23rwd23',
        SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://kts_user:kts_pass@localhost:5432/kts"
    )

    @app.route('/hello')
    def hello():
        return 'hello'

    from app.auth import bp
    app.register_blueprint(bp)
    from app.parser import bp
    app.register_blueprint(bp)

    return app


app = create_app()
# if __name__ == "__main":
#     app.run(debug=True)
app.run(debug=True)




# from app.db import run_db
#
# db = run_db(app)




#     # app.config.from_pyfile('config.py', silent=True)
#
#     # try:
#     #     os.makedirs(app.instance_path)
#     # except OSError:
#     #     pass
#
