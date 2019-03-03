from wtforms import Form, StringField

class SearchForm(Form):
    search = StringField('')