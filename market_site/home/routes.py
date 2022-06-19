from flask import render_template, Blueprint
from market_site import db
from market_site.models import *
from market_site.config import *
from flask_login import login_required, current_user

home = Blueprint("home", __name__)

@home.route('/home/assets')
@login_required
def home_assets():
	return render_template('home/assets.html', title='My assets')

@home.route('/home/assets/h')
@login_required
def home_hard_assets():
	return render_template('home/hard_assets.html', title='Hard assets')

@home.route('/home/assets/l')
@login_required
def home_liquid_assets():
	return render_template('home/liquid_assets.html', title='Liquid assets')

@home.route('/home/assets/l/shares')
@login_required
def home_shares():
	return render_template('home/shares.html', title='Shares')

@home.route('/home/assets/l/bonds')
@login_required
def home_bonds():
	return render_template('home/bonds.html', title='Bonds')



@home.route('/home/auctions')
@login_required
def home_auctions():
	auctions = db.session.query(Auction)\
		.where(Auction.seller_id == current_user.id).all()
	return render_template('home/auctions.html', title='Auctions', auctions=auctions)

@home.route('/home/sales')
@login_required
def home_sales():
	return render_template('home/sales.html', title='Sales sales')

@home.route('/home/sales/asset/h')
@login_required
def home_hsales():
	return render_template('home/hard_assets_sales.html', title='Sales hard sales')

@home.route('/home/sales/asset/l')
@login_required
def home_lsales():
	return render_template('home/liquid_assets_sales.html', title='Sales liquid sales')



@home.route('/home/loans')
@login_required
def home_loans():
	return render_template('home/loans.html', title='Loans')

@home.route('/home/loans/bank')
@login_required
def home_bank_loans():
	return render_template('home/bank_loans.html', title='Bank loans')

@home.route('/home/loans/personal')
@login_required
def home_personal_loans():
	return render_template('home/personal_loans.html', title='Personal loans')



@home.route('/home/transactions')
@login_required
def home_transactions():
	return render_template('home/transactions.html', title='Transactions')

@home.route('/home/transactions/made')
@login_required
def home_transactions_made():
	return render_template('home/transactions_made.html', title='Transactions made')

@home.route('/home/transactions/received')
@login_required
def home_transactions_received():
	return render_template('home/transactions_received.html', title='Transactions received')
