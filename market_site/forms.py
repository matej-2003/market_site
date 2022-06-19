from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DecimalField, SelectField
from wtforms.fields.html5 import DateTimeField
# from wtforms.validators import DataRequired, Length, Email, EqualTo
from market_site.models import Bank

class TransactionForm(FlaskForm):
    amount = DecimalField('Amount', places=2, rounding=None)
    receipient_id = IntegerField('Receipient id')
    submit = SubmitField('Confirm the payment')

class HardAssetSaleForm(FlaskForm):
    price = DecimalField('Price', places=2, rounding=None)
    submit = SubmitField('Confirm sale')

class AuctionForm(FlaskForm):
    price = DecimalField('Price', places=2, rounding=None)
    initial_price = DecimalField('Initial price', places=2, rounding=None)
    security_deposit = DecimalField('Security deposit', places=2, rounding=None)
    start = DateTimeField('Start auction', format='%d/%m/%Y %H:%M:%S')
    end = DateTimeField('End auction', format='%d/%m/%Y %H:%M:%S')
    bank = SelectField('Bank', choices=[(i.name, i.id) for i in Bank.query.all()])
    submit = SubmitField('Create auction')

class AuctionBidForm(FlaskForm):
    amount = DecimalField('Amount', places=2, rounding=None)
    submit = SubmitField('Bid')