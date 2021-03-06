from flask import render_template, url_for, flash, redirect, request, Blueprint
from market_site import bc, db
from market_site.users.forms import LoginForm, TransactionForm
from market_site.models import User
from market_site.config import PHYSICAL_PERSON, TRANSACTIO_ERROR
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

users = Blueprint("users", __name__, template_folder="templates")

@users.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if not user:
			flash('user not found!!!', 'error')
			return redirect(url_for('users.login'))

		if bc.check_password_hash(user.password, form.password.data):
			user.last_login = datetime.now()
			db.session.commit()

			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			else:
				# return redirect(url_for('home.home'))
				return redirect('/home')
		else:
			flash('Login unsucessfull!', 'error')

	return render_template('login.html', title='', form=form)

@users.route('/make_transaction', methods=['GET', 'POST'])
@login_required
def make_transaction():
	form = TransactionForm()
	receipient_id = request.args.get('receipient_id', None, type=int)
	amount = request.args.get('amount', None, type=float)

	if receipient_id:
		form.receipient_id.data = receipient_id
	if amount:
		form.amount.data = amount

	if form.validate_on_submit():
		user = User.query.get(form.receipient_id.data)
		if not user or receipient_id == current_user.id:
			flash('user not found!!!', 'error')
			redirect(url_for('users.make_transaction'))

		if not (form.amount.data > 0 and form.amount.data <= current_user.balance):
			flash('amount error amount must > 0 and smaller than your balance', 'error')
			redirect(url_for('users.make_transaction'))
		result = current_user.pay(float(form.amount.data), user, info=form.info.data)
		if result == TRANSACTIO_ERROR:
			flash(result, 'error')
		else:
			flash(result, 'success')
	return render_template('transaction/make_transaction.html', title='Make Transaction', form=form)


@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('users.login'))


@users.route('/users', methods=['POST', 'GET'])
@login_required
def user_list():
	page = request.args.get('page', 1, type=int)
	# users = User.query.filter_by(type=PHYSICAL_PERSON)\
	# 		.paginate(page=page, per_page=15)
	users = User.query.paginate(page=page, per_page=15)
	return render_template('user/users.html', title='Users', users=users)

@users.route('/user/<int:user_id>', methods=['POST', 'GET'])
@login_required
def user(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user/user.html', title='User ' + user.username, user=user)




@users.route('/user/<int:user_id>/h')
@login_required
def user_hard_assets(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user/hard_assets.html', title='Hard assets', user=user)

@users.route('/user/<int:user_id>/l')
@login_required
def user_liquid_assets(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user/liquid_assets.html', title='Liquid assets', user=user)

@users.route('/user/<int:user_id>/l/shares')
@login_required
def user_shares(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user/shares.html', title='Shares', user=user)

@users.route('/user/<int:user_id>/l/bonds')
@login_required
def user_bonds(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user/bonds.html', title='Bonds', user=user)



@users.route('/user/<int:user_id>/auctions')
@login_required
def user_auctions(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user/auctions.html', title='Auctions', user=user)

@users.route('/user/<int:user_id>/sales')
@login_required
def user_sales(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user/sales.html', title='Sales sales', user=user)

@users.route('/user/<int:user_id>/sales/asset/h')
@login_required
def user_hsales(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user/hard_assets_sales.html', title='Sales hard sales', user=user)

@users.route('/user/<int:user_id>/sales/asset/l')
@login_required
def user_lsales(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user/liquid_assets_sales.html', title='Sales liquid sales', user=user)



@users.route('/user/<int:user_id>/loans')
@login_required
def user_loans(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user/loans.html', title='Loans', user=user)

@users.route('/user/<int:user_id>/loans/bank')
@login_required
def user_bank_loans(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user/bank_loans.html', title='Bank loans', user=user)

@users.route('/user/<int:user_id>/loans/personal')
@login_required
def user_personal_loans(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user/personal_loans.html', title='Personal loans', user=user)



@users.route('/user/<int:user_id>/transactions')
@login_required
def user_transactions(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user/transactions.html', title='Transactions', user=user)

@users.route('/user/<int:user_id>/transactions/made')
@login_required
def user_transactions_made(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user/transactions_made.html', title='Transactions made', user=user)

@users.route('/user/<int:user_id>/transactions/received')
@login_required
def user_transactions_received(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user/transactions_received.html', title='Transactions received', user=user)