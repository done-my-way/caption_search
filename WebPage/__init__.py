from flask import Flask
from WebPage.forms import SearchForm
from flask import request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)

@app.route('/results')
def search_results(search):
    search_string = str(search.data['search'])
    return search_string
