from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from werkzeug.security import generate_password_hash, check_password_hash


class UserForm(FlaskForm):
    name = StringField('Username')
    hash = StringField('Password')


