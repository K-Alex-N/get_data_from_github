# from flask import Flask, render_template
#
#
# def run_flask(app: 'Flask'):
#     # DATABASE_URI = os.environ.get('DATABASE_URI')
#     app.config['DEBUG'] = True
#     app.config['SECRET_KEY'] ='aasd342!#ksmdfow884ht37chw2r92ur2'
#     # app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.sqlite3'
#
#     menu = ["Установка", "Первое приложение", "Обратная связь"]
#
#     @app.route('/')
#     def index():
#         return render_template('parcing_lists.html', title='Парсер GitHub', menu=menu)
#
#     app.run()
