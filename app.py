from flask import Flask, render_template, request
from googletrans import Translator
import re
import requests
from flask_wtf import FlaskForm
from wtforms import SelectField, BooleanField, RadioField
import os
from flask_babel import Babel, gettext as _

SECRET_KEY = os.urandom(32)


curr_language = 'en'
words_count = 40
punctuation = False

def generate_text(language, words_count, punct):
    url = "https://fish-text.ru/get?&number=8"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['text']

        if (language == 'en'):
            translator = Translator()
            data = translator.translate(data, dest='en')
            data = data.text

        if not punct:
            data = re.sub(r'[^\w\s]', '', data)

        test_text = " ".join(data.split()[:words_count])
    return test_text


def get_locale():
    translations = [str(translation) for translation in babel.list_translations()]
    return request.accept_languages.best_match(translations)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
#app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
babel = Babel(app)
babel.init_app(app, locale_selector=get_locale)

class Buttons(FlaskForm):
    language = SelectField(_('Language'),
                           choices=[('en', 'English'), ('ru', 'Russian')],
                           default='en')
    punct = BooleanField(_('Punctuation'), default=False)
    word = RadioField(_('Word Count'),
                      choices=[(10, 10), (40, 40), (100, 100)],
                      default=40)


@app.route('/', methods=['GET', 'POST'])



def home():
    global curr_language, punctuation, words_count
    if request.method == 'POST':
        buttons = Buttons(request.form)
        new_language = str(buttons.language.data)
        new_punctuation = bool(buttons.punct.data)
        new_word_cnt = int(buttons.word.data)
        if (new_language != curr_language
                or new_punctuation != punctuation
                or new_word_cnt != words_count):
            curr_language = new_language
            punctuation = new_punctuation
            words_count = new_word_cnt
            test_text = generate_text(curr_language, words_count, punctuation)
            return render_template('home.html',
                                   title=_("Print Speed Test"),
                                   instruction=_("Type the following text as quickly and accurately as you can:"),
                                   label_input = _("Your input:"),
                                   submit_button = _("Submit"),
                                   test_text=test_text,
                                   buttons=buttons)

        test_text = request.form['test_text']
        user_text = request.form['user_text']
        result = calculate_result(test_text, user_text)
        return render_template('result.html', result=result)

    if request.method == 'GET':
        buttons = Buttons(request.form)
        test_text = generate_text(curr_language, words_count, punctuation)

        return render_template('home.html',
                                title=_("Print Speed Test"),
                                instruction=_("Type the following text as quickly and accurately as you can:"),
                                label_input = _("Your input:"),
                                submit_button = _("Submit"),
                                test_text=test_text,
                                buttons=buttons)


def calculate_result(test_text, user_text):
    test_words = test_text.split()
    user_words = user_text.split()
    correct_words = [t for t, u in zip(test_words, user_words) if t == u]
    accuracy = len(correct_words) / len(test_words) * 100
    return accuracy

if __name__ == '__main__':
    app.run(debug=True)
