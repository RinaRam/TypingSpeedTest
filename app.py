from flask import Flask, render_template, request
from googletrans import Translator
import re
import requests
from flask_wtf import Form
from wtforms import SelectField


app = Flask(__name__)

class Buttons(Form):
    language = SelectField('Language', choices=[('en', 'English'), ('ru', 'Russian')], default='en')

@app.route('/', methods=['GET', 'POST'])
def home():
    buttons = Buttons()

    if request.method == 'POST':
        test_text = request.form['test_text']
        user_text = request.form['user_text']
        result = calculate_result(test_text, user_text)
        return render_template('result.html', result=result)
    
    words_count = 100
    language = 'en'
    if buttons.validate():
        language = str(buttons.language.data)
    punctuation = True #False

    url = "https://fish-text.ru/get?&number=8"
    response = requests.get(url)

    if response.status_code == 200:
        
        
        data = response.json()['text']
        if (language == 'en'):
            translator = Translator()
            data = translator.translate(data, dest='en')
            data = data.text        

        if not punctuation:
            data = re.sub(r'[^\w\s]', '', data) 
        
        test_text = " ".join(data.split()[:words_count])
        

    return render_template('home.html', test_text=test_text, buttons=buttons)

def calculate_result(test_text, user_text):
    test_words = test_text.split()
    user_words = user_text.split()
    correct_words = [t for t, u in zip(test_words, user_words) if t == u]
    accuracy = len(correct_words) / len(test_words) * 100
    return accuracy

if __name__ == '__main__':
    app.run(debug=True)
