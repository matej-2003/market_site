from flask_wtf import FlaskForm
from wtforms import *
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max=20)])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

# class TransactionForm(FlaskForm):
#     amount = DecimalField('Amount', places=2, rounding=None)
#     receipient_id = IntegerField('Receipient id')
#     submit = SubmitField('Confirm the payment')