from flask import Blueprint

bp = Blueprint('auth', __name__)

@app.route('/')
def parcing_lists_page():
    # return render_template('parcing_lists.html')
    return render_template('base.html')

# @app.route('/<int:parcing_id>')
# def parcing_data_page(parcing_id):
#     return render_template('parcing_lists.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('exeption/page404.html'), 404

def check_data(form):
    error = []
    if not form['name']:
        error.append('введите название')
    links = form['links']
    if not links:
        error.append('введите ссылки на репозитории')
    else:
        for link in links:
            if 'https://github.com' not in link:
                error.append('введите полную ссылку на репозиторий (пример https://github.com/django/django)')
                break
    return '\n'.join(error)

@app.route('/add', methods=['POST', 'GET'])
def add_new_parcing():
    if request.method == 'POST':
        error = check_data(request.form)
        if error:
            flash(error)
            return render_template('app/add_new_parcing.html')

        pull_request = PullRequest(
            name=request.form['name'],
            start_date=datetime.datetime.now(),
            frequency=request.form['frequency'],
        )
        app.db.session.add(pull_request)
        app.db.session.commit()

        for link in request.form['links'].split():
            url = Url(
                pull_request_id=pull_request.id,
                url=link
            )
            app.db.session.add(url)
        app.db.session.commit()
        # дб пересылка на страницу пользователя, а точнее на страницу данного задания на парсинг в странице пользователя
        # return redirect(url_for("parse_details", id=pull_request.id))

    return render_template('app/add_new_parcing.html')