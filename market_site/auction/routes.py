from flask import render_template, Blueprint, flash, redirect, request, url_for
from market_site.config import *
from market_site.models import *
from flask_login import current_user, login_required
# from datetime import datetime

auction = Blueprint("auction", __name__, template_folder="templates")

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



@auction.route('/auction/<int:auction_id>', methods=['GET', 'POST'])
@login_required
def auction_page(auction_id):
	auction = Auction.query.get_or_404(auction_id)
	if auction.is_bidder(current_user):
		if request.method == 'POST':
			bid_amount = float(request.form.get('bid_amount'))
			bid_submit = request.form.get('bid_submit')
			auction_unjoin = request.form.get('auction_unjoin')
			# print(bid_amount, bid_submit, auction_unjoin)
			try:
				bid_amount = float(bid_amount)
				if bid_amount and bid_submit:
					if bid_amount > auction.final_price:
						auction.place_bid(current_user, bid_amount)
				if auction_unjoin:
					auction.remove_bidder(current_user)
					return redirect(url_for('auction.join_auction', auction_id=auction_id))
			except ValueError:
				flash('error', 'error')
		return render_template('auction/auction.html', title='Auction', auction=auction)
	return redirect(url_for('auction.join_auction', auction_id=auction_id))


@auction.route('/auction/<int:auction_id>/edit', methods=['POST', 'GET'])
@login_required
def auction_edit(auction_id):
	return render_template('auction/edit.html', title='Auction edit')


@auction.route('/auction/<int:auction_id>/delete', methods=['POST', 'GET'])
@login_required
def auction_delete(auction_id):
	return redirect('/home')


@auction.route('/auction/<int:auction_id>/join', methods=['GET', 'POST'])
@login_required
def join_auction(auction_id):
	auction = Auction.query.get_or_404(auction_id)
	if request.method == 'POST':
		agree_to_terms = request.form.get('agree_to_terms')
		agree_to_commission = request.form.get('agree_to_commission')
		if agree_to_terms and agree_to_commission:
			auction.add_bidder(current_user)
		return redirect(url_for('auction.auction_page', auction_id=auction_id))
	return render_template('auction/join_auction.html', title='Auction', auction=auction)


@auction.route('/auction/<int:auction_id>/history', methods=['GET', 'POST'])
@login_required
def auction_history(auction_id):
	auction = Auction.query.get_or_404(auction_id)
	return render_template('auction/history.html', title='Auction', auction=auction)
