from flask import Flask, render_template, request, session
import re
import requests
from flask_wtf import FlaskForm
from wtforms import SelectField, BooleanField, RadioField
import os
from flask_babel import Babel, lazy_gettext as _, force_locale
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SECRET_KEY = os.urandom(32)


def generate_text(language, words_count, punct):
    if (language == 'en'):
        url = "https://generatefakename.com/text"
        data = ""
        for i in range(3):
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                data += soup.find_all('h3')[0].get_text() + " "

        if not punct:
            data = re.sub(r'[^\w\s]', ' ', data[:-1])

        test_text = " ".join(data.split()[:words_count])
    else: 
        url = "https://fish-text.ru/get?&number=8"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()['text']

            if not punct:
                data = re.sub(r'[^\w\s]', '', data)

            test_text = " ".join(data.split()[:words_count])
    return test_text


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

class Buttons(FlaskForm):
    language = SelectField(_('Language'),
                           choices=[('ru', 'Русский'),('en', 'English')],
                           default='en')
    punct = BooleanField(_('Punctuation'), default=False)
    word = RadioField(_('Word Count'),
                      choices=[(10, 10), (40, 40), (100, 100)],
                      default=40)
    sec = RadioField(_('Seconds'),
                      choices=[(10, 10), (30, 30), (60, 60)],
                      default=60)
    


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        buttons = Buttons(request.form)
        new_language = str(buttons.language.data)
        new_punctuation = bool(buttons.punct.data)
        new_word_cnt = int(buttons.word.data)

        if (request.form.get('submit_button') != None):
            user_text = request.form['user_text']
            test_text = session.get('test_text', '')
            result = calculate_result(test_text, user_text)
            return render_template('result.html', result=round(result, 2),
                                                  user_words=user_text.split(),
                                                  correct_words=test_text.split(),
                                                  time=request.form['submit_button'], 
                                                  entered_words_number=len(user_text.split()))
                
        if (new_language != session.get('curr_language', 'en') 
                    or new_punctuation != session.get('punctuation', False)
                    or new_word_cnt != session.get('words_count', 40)):
            
            session['curr_language'] = new_language
            session['punctuation'] = new_punctuation
            session['words_count'] = new_word_cnt
            session['test_text'] = generate_text(session['curr_language'], session['words_count'], session['punctuation'])
            
            return render_template('home.html',
                                   title=_('Print Speed Test'),
                                   instruction=_('Type the following text as quickly and accurately as you can:'),
                                   label_input = _('Your input:'),
                                   submit_button = _('Submit'),
                                   test_text=session['test_text'],
                                   buttons=buttons)
        

    if request.method == 'GET':
        buttons = Buttons(request.form)
        session['curr_language'] = 'en'
        session['punctuation'] = False
        session['words_count'] = 40
        session['test_text'] = generate_text(session['curr_language'], session['words_count'], session['punctuation'])

        return render_template('home.html',
                                        title=_("Print Speed Test"),
                                        instruction=_("Type the following text as quickly and accurately as you can:"),
                                        label_input = _("Your input:"),
                                        submit_button = _("Submit"),
                                        test_text=session['test_text'],
                                        buttons=buttons)

@app.route('/home2', methods=['GET', 'POST'])
def maxWordFixedTime():
    global curr_language, punctuation, sec, test_text
    
    if request.method == 'POST':
        buttons = Buttons(request.form)
        new_language = str(buttons.language.data)
        new_punctuation = bool(buttons.punct.data)
        new_sec = int(buttons.sec.data)
        if (request.form.get('submit_button') != None):
            user_text = request.form['user_text']
            test_text = session.get('test_text', '')
            result = calculate_result(test_text, user_text)
            return render_template('result2.html', result=round(result, 2),
                                                  user_words=user_text.split(),
                                                  correct_words=test_text.split(),
                                                  time=session.get('sec', 60), 
                                                  entered_words_number=len(user_text.split()))
        
        if (new_language != session.get('curr_language', 'en') 
                    or new_punctuation != session.get('punctuation', False)
                    or new_sec != session.get('sec', 60)):
            
            session['curr_language'] = new_language
            session['punctuation'] = new_punctuation
            session['sec'] = new_sec
            session['test_text'] = generate_text(session['curr_language'], session['words_count'], session['punctuation'])
            with force_locale(session['curr_language']):
                return render_template('maxWordFixedTime.html',
                                        title=_('Print Speed Test'),
                                        instruction=_('Type the following text as quickly and accurately as you can:'),
                                        label_input = _('Your input:'),
                                        submit_button = _('Submit'),
                                        test_text=session['test_text'],
                                        buttons=buttons,
                                        sec=session['sec'])
        print("HERE")        
        # test_text = request.form['test_text'] ## No .form['test_text'] in 'POST'
        user_text = request.form['user_text']
        result = calculate_result(session['test_text'], user_text)
        return render_template('result2.html', result=result)

    if request.method == 'GET':
        buttons = Buttons(request.form)
        session['curr_language'] = 'en'
        session['punctuation'] = False
        session['words_count'] = 100
        session['sec'] = 60
        session['test_text'] = generate_text(session['curr_language'], session['words_count'], session['punctuation'])

        with force_locale(session['curr_language']):
            return render_template('maxWordFixedTime.html',
                                        title=_("Print Speed Test"),
                                        instruction=_("Type the following text as quickly and accurately as you can:"),
                                        label_input = _("Your input:"),
                                        submit_button = _("Submit"),
                                        test_text=session['test_text'],
                                        buttons=buttons,
                                        sec=session['sec'])

@app.route('/result2', methods=['GET', 'POST'])
def result():
    return "result2"

def calculate_result(test_text, user_text):
    test_words = test_text.split()
    user_words = user_text.split()
    correct_words = [t for t, u in zip(test_words, user_words) if t == u]
    accuracy = len(correct_words) / len(test_words) * 100
    return accuracy

if __name__ == '__main__':
    app.run(debug=True)
