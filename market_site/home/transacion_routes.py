from flask import render_template, Blueprint, request
from market_site import db
from market_site.models import *
from market_site.config import *
from . import home
from flask_login import login_required, current_user
from flask_breadcrumbs import register_breadcrumb
from sqlalchemy import or_


@home.route('/transactions')
@login_required
@register_breadcrumb(home, '.home_transactions', 'Transactions')
def home_transactions():
	page = request.args.get('page', 1, type=int)
	transactions = db.session.query(Transaction)\
		.where(or_(Transaction.payee_id == current_user.id, Transaction.payer_id == current_user.id))\
		.order_by(Transaction.time.desc())\
		.paginate(page=page, per_page=20)
	return render_template('home/transactions/transactions.html', title='Transactions', transactions=transactions)

@home.route('/transactions/made')
@login_required
@register_breadcrumb(home, '.home_transactions.home_transactions_made', 'Made')
def home_transactions_made():
	page = request.args.get('page', 1, type=int)
	transactions = db.session.query(Transaction)\
		.where(Transaction.payee_id == current_user.id)\
		.order_by(Transaction.time.desc())\
		.paginate(page=page, per_page=20)
	return render_template('home/transactions/transactions.html', title='Transactions', transactions=transactions)

@home.route('/transactions/received')
@login_required
@register_breadcrumb(home, '.home_transactions.home_transactions_received', 'Received')
def home_transactions_received():
	page = request.args.get('page', 1, type=int)
	transactions = db.session.query(Transaction)\
		.where(Transaction.payer_id == current_user.id)\
		.order_by(Transaction.time.desc())\
		.paginate(page=page, per_page=20)
	# print(transactions.pages)
	return render_template('home/transactions/transactions.html', title='Transactions', transactions=transactions)