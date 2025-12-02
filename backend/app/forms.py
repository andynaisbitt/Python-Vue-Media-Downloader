from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class DownloadForm(FlaskForm):
    urls = TextAreaField('YouTube URLs (one per line)', validators=[DataRequired()])
    submit = SubmitField('Download')
