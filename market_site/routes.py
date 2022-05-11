from flask import render_template, url_for, flash, redirect, request, Response
from market_site import PHYSICAL_PERSON, app, bc, db, TRANSACTIO_ERROR
from market_site.forms import LoginForm
from market_site.models import User, Bank
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import json

@app.route('/')
@app.route('/home')
@login_required
def home():
	return render_template('index.html', title='Home')

@app.route('/user_assets')
@login_required
def user_assets():
	return render_template('user_assets.html', title='User assets')

@app.route('/users', methods=['POST', 'GET'])
@login_required
def users():
	users = User.query.filter_by(type=PHYSICAL_PERSON).all()
	return render_template('users.html', title='Users', users=users)

@app.route('/user/<int:user_id>', methods=['POST', 'GET'])
@login_required
def user(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user.html', title='User ' + user.username, user=user)

@app.route('/api/user/<int:user_id>/hard_assets')
@login_required
def api_user_hard_assets(user_id):
	user = User.query.get_or_404(user_id)
	data = []
	for hard_asset in user.hard_assets:
		data.append(hard_asset.objectify())
	return Response(json.dumps(data), mimetype='text/json')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if not user:
			flash('user not found!!!', 'error')
			return redirect(url_for('login'))
	
		if bc.check_password_hash(user.password, form.password.data):
			user.last_login = datetime.utcnow()
			db.session.commit()
			
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			else:
				return redirect(url_for('home'))
		else:
			flash('Login unsucessfull!', 'error')

	return render_template('login.html', title='', form=form, not_show_nav=True)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))


@app.route('/transaction', methods=['POST', 'GET'])
@login_required
def transaction():
	if request.method == 'POST':
		receipient_id = request.form.get('receipient_id')
		amount = request.form.get('amount')
		try:
			receipient = User.query.get_or_404(receipient_id)
			amount = float(amount)
			if receipient and amount > 0:
				if current_user.pay(amount, receipient) == TRANSACTIO_ERROR:
					flash('You can not make a transfer to thos account')
				return redirect('/')
		except ValueError:
			print("error")
	return render_template('transaction.html', title='Make Payment')

@app.route('/borrow', methods=['POST', 'GET'])
@login_required
def borrow():
	banks = Bank.query.all()
	return render_template('/borrow/banks.html', title='Borrow', banks=banks)

@app.route('/borrow/bank/<int:bank_id>', methods=['POST', 'GET'])
@login_required
def bank(bank_id):
	bank = Bank.query.get_or_404(bank_id)
	return render_template('/borrow/bank.html', title='Bank', bank=bank)

@app.route('/borrow/bank/<int:bank_id>/loan', methods=['POST', 'GET'])
@login_required
def loan(bank_id):
	bank = Bank.query.get_or_404(bank_id)
	return render_template('/borrow/loan.html', title='Loan', bank=bank)