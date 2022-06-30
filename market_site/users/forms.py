from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, IntegerField
from wtforms.fields import TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Optional

class TransactionForm(FlaskForm):
    receipient_id = IntegerField('Receipient id', validators=[DataRequired(), NumberRange(min=1)])
    amount = DecimalField('Amount', places=2, rounding=None, validators=[DataRequired(), NumberRange(min=0.01)])
    info = TextAreaField('Aditional info', [Optional(), Length(max=200)])
    submit = SubmitField('Confirm the payment')


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