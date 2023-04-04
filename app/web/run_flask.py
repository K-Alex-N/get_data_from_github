from flask import Flask, render_template


def run_flask():
    app = Flask(__name__)
    app.run()

    menu = ["Установка", "Первое приложение", "Обратная связь"]

    @app.route('/')
    def index():
        return render_template('index.html', title='Парсер GitHub', menu=menu)

