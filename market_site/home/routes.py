from flask import render_template, Blueprint, request
from market_site import db
from market_site.models import *
from market_site.config import *
from flask_login import login_required, current_user
from sqlalchemy import or_

home = Blueprint("home", __name__, url_prefix="/home", template_folder="templates")

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
	page = request.args.get('page', 1, type=int)
	hard_assets = db.session.query(HardAsset)\
		.where(HardAsset.owner_id == current_user.id)\
		.paginate(page=page, per_page=6)
	return render_template('home/hard_assets.html', title='Hard assets', hard_assets=hard_assets)

@home.route('/assets/l')
@login_required
def home_liquid_assets():
	return render_template('home/liquid_assets.html', title='Liquid assets')

@home.route('/assets/l/stock')
@login_required
def home_stock():
	page = request.args.get('page', 1, type=int)
	stock = current_user.shares_().paginate(page=page, per_page=5)
	return render_template('home/stock.html', title='Stock', stock=stock)

@home.route('/assets/l/bonds')
@login_required
def home_bonds():
	page = request.args.get('page', 1, type=int)
	bonds = current_user.bonds_().paginate(page=page, per_page=5)
	return render_template('home/bonds.html', title='Bonds', bonds=bonds)





@home.route('/auctions')
@login_required
def home_auctions():
	auctions = db.session.query(Auction)\
		.where(Auction.seller_id == current_user.id).all()
	return render_template('home/auctions.html', title='Auctions', auctions=auctions)



@home.route('/auctions/sale')
@login_required
def home_sale_auctions():
	return render_template('home/sales_auction.html', title='Sales auctions')


@home.route('/auctions/sale/active')
@login_required
def home_sale_auctions_active():
	auctions = db.session.query(Auction)\
		.where(Auction.seller_id == current_user.id)\
		.where(Auction.is_over(Auction) == False).all()
	return render_template('home/sales_auctions.html', title='Active sales auctions', auctions=auctions)

@home.route('/auctions/sale/finnished')
@login_required
def home_sale_auctions_finnished():
	auctions = db.session.query(Auction)\
		.where(Auction.seller_id == current_user.id)\
		.where(Auction.is_over(Auction) == True).all()
	return render_template('home/sales_auctions.html', title='Finnished sales auctions', auctions=auctions)


@home.route('/auctions/purchase')
@login_required
def home_purchase_auctions():
	return render_template('home/purchase_auction.html', title='Purchases auctions')


@home.route('/auctions/purchase/active')
@login_required
def home_purchase_auctions_active():
	auctions = db.session.query(Auction)\
		.where(Auction.buyer_id == current_user.id)\
		.where(Auction.is_over(Auction) == False).all()
	return render_template('home/purchase_auctions.html', title='Active purchase auctions', auctions=auctions)

@home.route('/auctions/purchase/finnished')
@login_required
def home_purchases_auctions_finnished():
	auctions = db.session.query(Auction)\
		.where(Auction.buyer_id == current_user.id)\
		.where(Auction.is_over(Auction) == True).all()
	return render_template('home/purchase_auctions.html', title='Finnished purchase auctions', auctions=auctions)





@home.route('/sales')
@login_required
def home_sales():
	return render_template('home/sales.html', title='Sales')

@home.route('/sales/asset/h')
@login_required
def home_hsales():
	sales = db.session.query(HardAssetSale)\
			.where(HardAssetSale.seller_id == current_user.id).all()
	purchases = db.session.query(HardAssetSale)\
			.where(HardAssetSale.buyer_id == current_user.id).all()
	return render_template('home/hard_assets_sales.html', title='Hard assets sales', sales=sales, purchases=purchases)

@home.route('/sales/asset/l')
@login_required
def home_lsales():
	return render_template('home/liquid_assets_sales.html', title='Liquid assets sales')


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
	loans = db.session.query(BankLoan, Bank, HardAsset)\
			.join(Bank, BankLoan.bank_id == Bank.id)\
			.join(HardAsset, BankLoan.hard_asset_id == HardAsset.id)\
			.where(BankLoan.borrower_id == current_user.id).all()
	return render_template('home/bank_loans.html', title='Bank loans', loans=loans)

@home.route('/loans/personal')
@login_required
def home_personal_loans():
	return render_template('home/personal_loans.html', title='Personal loans')



@home.route('/transactions')
@login_required
def home_transactions():
	page = request.args.get('page', 1, type=int)
	transactions = db.session.query(Transaction)\
		.where(or_(Transaction.payee_id == current_user.id, Transaction.payer_id == current_user.id))\
		.order_by(Transaction.time.desc())\
		.paginate(page=page, per_page=20)
	return render_template('home/transactions.html', title='Transactions', transactions=transactions)

@home.route('/transactions/made')
@login_required
def home_transactions_made():
	page = request.args.get('page', 1, type=int)
	transactions = db.session.query(Transaction)\
		.where(Transaction.payee_id == current_user.id)\
		.order_by(Transaction.time.desc())\
		.paginate(page=page, per_page=20)
	return render_template('home/transactions.html', title='Transactions', transactions=transactions)

@home.route('/transactions/received')
@login_required
def home_transactions_received():
	page = request.args.get('page', 1, type=int)
	transactions = db.session.query(Transaction)\
		.where(Transaction.payer_id == current_user.id)\
		.order_by(Transaction.time.desc())\
		.paginate(page=page, per_page=20)
	# print(transactions.pages)
	return render_template('home/transactions.html', title='Transactions', transactions=transactions)