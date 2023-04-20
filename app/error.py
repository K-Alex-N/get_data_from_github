from flask import Blueprint, render_template

error = Blueprint('error', __name__)

@error.errorhandler(404)
def page_not_found(error):
    return render_template('error/page404.html'), 404