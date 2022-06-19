from flask import render_template, Blueprint, flash, redirect, request
from market_site import bc, db
from market_site.forms import LoginForm
from market_site.config import *
from market_site.models import *
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

auction = Blueprint("auction", __name__)

@auction.route('/borrow', methods=['POST', 'GET'])
@login_required
def borrow():
	banks = Bank.query.all()
	return render_template('/borrow/banks.html', title='Borrow', banks=banks)

@auction.route('/borrow/bank/<int:bank_id>', methods=['POST', 'GET'])
@login_required
def bank(bank_id):
	bank = Bank.query.get_or_404(bank_id)
	return render_template('/borrow/bank.html', title='Bank', bank=bank)

@auction.route('/borrow/bank/<int:bank_id>/loan', methods=['POST', 'GET'])
@login_required
def loan(bank_id):
	bank = Bank.query.get_or_404(bank_id)
	return render_template('/borrow/loan.html', title='Loan', bank=bank)




@auction.route('/transactions', methods=['POST', 'GET'])
@login_required
def make_transaction():
	if request.method == 'POST':
		receipient_id = request.form.get('receipient_id')
		amount = request.form.get('amount')
		try:
			receipient = User.query.get_or_404(receipient_id)
			amount = float(amount)
			if receipient and amount > 0:
				if current_user.pay(amount, receipient) == TRANSACTIO_ERROR:
					flash('You can not make a transfer to thos account', 'warning')
				return redirect('/')
		except ValueError:
			print("error")
	return render_template('transaction/transaction.html', title='Make Payment')


@auction.route('/transaction/<int:id>', methods=['POST', 'GET'])
@login_required
def transaction(id):
	return render_template('transaction/transaction.html', title=f'Transaction {id}')


@auction.route('/transactions', methods=['POST', 'GET'])
@login_required
def transactions():
	return render_template('transaction/transaction.html', title='Transactions')


@auction.route('/transactions/made', methods=['POST', 'GET'])
@login_required
def transactions_made():
	return render_template('transaction/made.html', title='Transactions made')


@auction.route('/transactions/received', methods=['POST', 'GET'])
@login_required
def transactions_received():
	return render_template('transactions/received.html', title='Transactions received')




@auction.route('/sale/<int:sale_id>/edit', methods=['POST', 'GET'])
@login_required
def sale_edit(sale_id):
	return render_template('sale/edit.html', title='Sale edit')

@auction.route('/sale/<int:sale_id>/delete', methods=['POST', 'GET'])
@login_required
def sale_delete(sale_id):
	return redirect('/home')


@auction.route('/auction/<int:auction_id>/edit', methods=['POST', 'GET'])
@login_required
def auction_edit(auction_id):
	return render_template('auction/edit.html', title='Auction edit')

@auction.route('/auction/<int:auction_id>/delete', methods=['POST', 'GET'])
@login_required
def auction_delete(auction_id):
	return redirect('/home')
