
from app.home import home
from flask import redirect, url_for


@home.route("/")
def index():
    return redirect(url_for('admin.login'))
