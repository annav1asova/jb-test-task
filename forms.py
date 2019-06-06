from wtforms import Form, StringField, TextField, validators, ValidationError
from flask import request
from character_utils import is_alpha, is_digit, is_allowed_special

class SearchForm(Form):
    q = StringField('search', validators=[validators.InputRequired(),
                                          # validators.Regexp('([a-zA-z0-9|_]+)'),
                                          ])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

    def is_correct(self):
        s = self.q.data.lower()
        return all(is_alpha(sym) or is_digit(sym) or is_allowed_special(sym) for sym in s)
