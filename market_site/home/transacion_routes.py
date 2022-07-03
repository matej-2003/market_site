from flask import render_template, request
from market_site import db
from market_site.models import *
from market_site.config import *
from . import home
from flask_login import login_required, current_user
from flask_breadcrumbs import register_breadcrumb


@home.route('/transactions')
@login_required
@register_breadcrumb(home, '.home_transactions', 'Transactions')
def home_transactions():
	return render_template('home/transactions/transactions_overview.html', title='Transactions')

def transaction_list(**kwargs):
	page = request.args.get('page', 1, type=int)
	user_sort = request.args.get('user_sort', type=int)
	amount_sort = request.args.get('amount_sort', type=str)
	time_sort = request.args.get('time_sort', 'desc', type=str)
	transactions = []

	if time_sort == 'asc':
		transactions = db.session.query(Transaction)\
			.where(Transaction.payer_id == current_user.id)\
			.order_by(Transaction.time.asc())\
			.paginate(page=page, per_page=30)
	else:
		transactions = db.session.query(Transaction)\
			.where(Transaction.payer_id == current_user.id)\
			.order_by(Transaction.time.desc())\
			.paginate(page=page, per_page=30)

	if amount_sort == 'desc':
		transactions = db.session.query(Transaction)\
			.where(Transaction.payer_id == current_user.id)\
			.order_by(Transaction.amount.desc())\
			.paginate(page=page, per_page=30)
	elif amount_sort == 'asc':
		transactions = db.session.query(Transaction)\
			.where(Transaction.payer_id == current_user.id)\
			.order_by(Transaction.amount.asc())\
			.paginate(page=page, per_page=30)

	if user_sort == 'desc':
		transactions = db.session.query(Transaction)\
			.where(Transaction.payer_id == current_user.id)\
			.order_by(Transaction.payer_id.desc())\
			.paginate(page=page, per_page=30)
	elif user_sort == 'asc':
		transactions = db.session.query(Transaction)\
			.where(Transaction.payer_id == current_user.id)\
			.order_by(Transaction.payer_id.asc())\
			.paginate(page=page, per_page=30)
	
	return render_template('home/transactions/transactions.html', transactions=transactions, **kwargs)

@home.route('/transactions/made')
@login_required
@register_breadcrumb(home, '.home_transactions.home_transactions_made', 'Made')
def home_transactions_made():
	return transaction_list(made=True, title='Transactions made')
	# return render_template('home/transactions/transactions.html', title='Transactions made', transactions=transactions, made=True)

@home.route('/transactions/received')
@login_required
@register_breadcrumb(home, '.home_transactions.home_transactions_received', 'Received')
def home_transactions_received():
	return transaction_list(title='Transactions received')
	# page = request.args.get('page', 1, type=int)
	# transactions = db.session.query(Transaction)\
	# 	.where(Transaction.payee_id == current_user.id)\
	# 	.order_by(Transaction.time.desc())\
	# 	.paginate(page=page, per_page=30)
	# return render_template('home/transactions/transactions.html', title='Transactions received', transactions=transactions)