from flask import Flask, request
from .pages import post_page, get_page
import os
from flask_babel import Babel
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SECRET_KEY = os.urandom(32)


def get_locale():
    """Функция получения значения установлненной локали"""
    return os.environ.get('LC_ALL', 'en_US.UTF-8')[:2]


app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)
app.config['SECRET_KEY'] = SECRET_KEY
babel = Babel(app)
babel.init_app(app, locale_selector=get_locale)


@app.route('/home', methods=['GET', 'POST'])
def home():
    """
    Функция отображения страницы /home, её результата 
    и обработки изменений на ней
    """
    if request.method == 'POST':
        return post_page('home.html', 'result.html')

    if request.method == 'GET':
        return get_page('home.html')


@app.route('/home2', methods=['GET', 'POST'])
def maxWordFixedTime():
    """
    Функция отображения страницы /home2, её результата 
    и обработки изменений на ней
    """
    if request.method == 'POST':
        return post_page('maxWordFixedTime.html', 'result2.html')

    if request.method == 'GET':
        return get_page('maxWordFixedTime.html')


if __name__ == '__main__':
    app.run(debug=True)

