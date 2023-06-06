from flask import Flask, request
from pages import post_result, post_page, get_page
import os
from flask_babel import Babel
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SECRET_KEY = os.urandom(32)

def get_locale():
    translations = [str(translation) for translation in babel.list_translations()]
    return request.accept_languages.best_match(translations)

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)
babel.init_app(app, locale_selector=get_locale)


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return post_page('home.html', 'result.html')

    if request.method == 'GET':
        return get_page('home.html')

@app.route('/home2', methods=['GET', 'POST'])
def maxWordFixedTime():
    if request.method == 'POST':
        return post_page('maxWordFixedTime.html', 'result2.html')

    if request.method == 'GET':
        return get_page('maxWordFixedTime.html')

if __name__ == '__main__':
    app.run(debug=True)



