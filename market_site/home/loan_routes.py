from flask import render_template, Blueprint, request
from market_site import db
from market_site.models import *
from market_site.config import *
from . import home
from flask_login import login_required, current_user
from flask_breadcrumbs import register_breadcrumb
from sqlalchemy import or_


@home.route('/loans')
@login_required
@register_breadcrumb(home, '.home_loans', 'Bond')
def home_loans():
	return render_template('home/loans/loans.html', title='Loans')

@home.route('/loans/bank')
@login_required
@register_breadcrumb(home, '.home_loans.home_bank_loans', 'Bank')
def home_bank_loans():
	loans = db.session.query(BankLoan, Bank, HardAsset)\
			.join(Bank, BankLoan.bank_id == Bank.id)\
			.join(HardAsset, BankLoan.hard_asset_id == HardAsset.id)\
			.where(BankLoan.borrower_id == current_user.id).all()
	return render_template('home/loans/bank_loans.html', title='Bank loans', loans=loans)

@home.route('/loans/personal')
@login_required
@register_breadcrumb(home, '.home_loans.home_personal_loans', 'Personal')
def home_personal_loans():
	return render_template('home/loans/personal_loans.html', title='Personal loans')
