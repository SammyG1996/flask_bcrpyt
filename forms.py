from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import InputRequired
from wtforms.widgets import PasswordInput


class AddRegisterForm(FlaskForm):
  '''This will contain the from to add new pets'''

  username = StringField('username', [InputRequired()])
  password = StringField('password', widget=PasswordInput(hide_value=False), validators=[InputRequired()])
  email = StringField('email', validators=[InputRequired()])
  first_name = StringField('first name', validators=[InputRequired()])
  last_name = StringField('last name', validators=[InputRequired()])



class LoginForm(FlaskForm):
  '''This will contain the from to add new pets'''

  username = StringField('username', [InputRequired()])
  password = StringField('password', widget=PasswordInput(hide_value=False), validators=[InputRequired()])