from flask import render_template, Blueprint
from market_site import db
from market_site.models import *
from market_site.config import *
from flask_login import login_required, current_user

home = Blueprint("home", __name__, url_prefix="/home", template_folder="templates")

# @home.route('/')
@home.route('/')
@login_required
def user_home():
	return render_template('home/home.html', title='Home')

@home.route('/assets')
@login_required
def home_assets():
	return render_template('home/assets.html', title='My assets')

@home.route('/assets/h')
@login_required
def home_hard_assets():
	return render_template('home/hard_assets.html', title='Hard assets')

@home.route('/assets/l')
@login_required
def home_liquid_assets():
	return render_template('home/liquid_assets.html', title='Liquid assets')

@home.route('/assets/l/shares')
@login_required
def home_shares():
	return render_template('home/shares.html', title='Shares')

@home.route('/assets/l/bonds')
@login_required
def home_bonds():
	return render_template('home/bonds.html', title='Bonds')



@home.route('/auctions')
@login_required
def home_auctions():
	auctions = db.session.query(Auction)\
		.where(Auction.seller_id == current_user.id).all()
	return render_template('home/auctions.html', title='Auctions', auctions=auctions)

@home.route('/auctions/active')
@login_required
def home_auctions_active():
	auctions = db.session.query(Auction)\
		.where(Auction.seller_id == current_user.id)\
		.where(Auction.is_over(Auction) == False).all()
	return render_template('home/auctions.html', title='Auctions', auctions=auctions)

@home.route('/auctions/finnished')
@login_required
def home_auctions_finnished():
	auctions = db.session.query(Auction)\
		.where(Auction.seller_id == current_user.id)\
		.where(Auction.is_over(Auction) == True).all()
	return render_template('home/auctions.html', title='Auctions', auctions=auctions)



@home.route('/sales')
@login_required
def home_sales():
	return render_template('home/sales.html', title='Sales sales')

@home.route('/sales/asset/h')
@login_required
def home_hsales():
	sales = db.session.query(HardAssetSale)\
			.where(HardAssetSale.seller_id == current_user.id).all()
	purchases = db.session.query(HardAssetSale)\
			.where(HardAssetSale.buyer_id == current_user.id).all()
	return render_template('home/hard_assets_sales.html', title='Sales hard sales', sales=sales, purchases=purchases)

@home.route('/sales/asset/l')
@login_required
def home_lsales():
	return render_template('home/liquid_assets_sales.html', title='Sales liquid sales')


@home.route('/sales/asset/l/stock')
@login_required
def home_stock_sales():
	sales = db.session.query(CompanyShareSale)\
			.where(CompanyShareSale.seller_id == current_user.id).all()
	purchases = db.session.query(CompanyShareSale)\
			.where(CompanyShareSale.buyer_id == current_user.id).all()
	return render_template('home/stock_sales.html', title='Stock sales', sales=sales, purchases=purchases)


@home.route('/sales/asset/l/bond')
@login_required
def home_bond_sales():
	sales = db.session.query(CompanyBondSale)\
			.where(CompanyBondSale.seller_id == current_user.id).all()
	purchases = db.session.query(CompanyBondSale)\
			.where(CompanyBondSale.buyer_id == current_user.id).all()
	return render_template('home/bond_sales.html', title='Bond sales', sales=sales, purchases=purchases)




@home.route('/loans')
@login_required
def home_loans():
	return render_template('home/loans.html', title='Loans')

@home.route('/loans/bank')
@login_required
def home_bank_loans():
	return render_template('home/bank_loans.html', title='Bank loans')

@home.route('/loans/personal')
@login_required
def home_personal_loans():
	return render_template('home/personal_loans.html', title='Personal loans')



@home.route('/transactions')
@login_required
def home_transactions():
	return render_template('home/transactions.html', title='Transactions')

@home.route('/transactions/made')
@login_required
def home_transactions_made():
	return render_template('home/transactions_made.html', title='Transactions made')

@home.route('/transactions/received')
@login_required
def home_transactions_received():
	return render_template('home/transactions_received.html', title='Transactions received')
