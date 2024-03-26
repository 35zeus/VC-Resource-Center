from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, DateField, TextAreaField, RadioField,
    FileField,
)
from wtforms.validators import InputRequired, ValidationError, DataRequired
from werkzeug.security import check_password_hash
from models import User


class UserForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    role = StringField('Role')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date')
    content_body = TextAreaField('Content Body', validators=[DataRequired()])
    content_body_post = TextAreaField('Content Body Post', validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired()])
    alt = StringField('Alt', validators=[DataRequired()])
    hours = StringField('Hours', validators=[DataRequired()])
    address_url = StringField('Address URL', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    vendors_needed = RadioField(
        label='Vendors Needed',
        validators=[DataRequired()],
        choices=[('True', 'Yes'), ('False', 'No')]
    )


class LoginForm(FlaskForm):
    login = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Sign In')

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise ValidationError('Invalid user')

        # we're comparing the plaintext pw with the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise ValidationError('Invalid password')

    def get_user(self):
        return User.query.filter_by(username=self.login.data).first()
