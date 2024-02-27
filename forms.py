from flask_wtf import FlaskForm
from wtforms import StringField


class UserForm(FlaskForm):
    name = StringField('Username')
    hash = StringField('Password')
