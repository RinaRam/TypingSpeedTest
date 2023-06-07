from flask import render_template, request, session
from wtforms import SelectField, BooleanField, RadioField
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _
from tools import generate_text, calculate_result


title = _('Print Speed Test')
instruction = _('Type the text as quickly and accurately as you can:')
label_input = _('Your input:')
submit_button = _('Submit')


class Buttons(FlaskForm):
    language = SelectField(_('Language'),
                           choices=[('ru', 'Русский'), ('en', 'English')],
                           default='en')
    punct = BooleanField(_('Punctuation'), default=False)
    word = RadioField(_('Word Count'),
                      choices=[(10, 10), (40, 40), (100, 100)],
                      default=40)
    sec = RadioField(_('Seconds'),
                     choices=[(10, 10), (30, 30), (60, 60)],
                     default=60)


def template_render(page_name, buttons):
    return render_template(page_name,
                           title=title,
                           instruction=instruction,
                           label_input=label_input,
                           submit_button=submit_button,
                           test_text=session['test_text'],
                           buttons=buttons,
                           sec=session['sec'])


def post_result(page_name):
    user_text = request.form['user_text']
    test_text = session.get('test_text', '')
    result = calculate_result(test_text, user_text)
    return render_template(page_name,
                           result=round(result, 2),
                           user_words=user_text.split(),
                           correct_words=test_text.split(),
                           time=request.form['submit_button']
                           if page_name == "result.html" else
                           session.get('sec', 60),
                           entered_words_number=len(user_text.split()))


def post_page(page_name, result_page_name):
    buttons = Buttons(request.form)
    new_language = str(buttons.language.data)
    new_punctuation = bool(buttons.punct.data)
    new_sec = int(buttons.sec.data)
    new_word_cnt = int(buttons.word.data)

    if (request.form.get('submit_button') is not None):
        return post_result(result_page_name)

    if (new_language != session.get('curr_language', 'en')
        or new_punctuation != session.get('punctuation', False)
        or (new_word_cnt != session.get('words_count', 40)
            if page_name == "home.html" else False)):

        session['curr_language'] = new_language
        session['punctuation'] = new_punctuation
        session['sec'] = new_sec
        session['words_count'] = new_word_cnt
        session['test_text'] = generate_text(session['curr_language'],
                                             session['words_count'],
                                             session['punctuation'])
        return template_render(page_name, buttons)


def get_page(page_name):
    buttons = Buttons(request.form)
    session['curr_language'] = 'en'
    session['punctuation'] = False
    session['words_count'] = 40
    session['sec'] = 60
    session['test_text'] = generate_text(session['curr_language'],
                                         session['words_count'],
                                         session['punctuation'])
    return template_render(page_name, buttons)
