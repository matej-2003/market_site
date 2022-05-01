from flask import render_template, url_for, flash, redirect, request, abort
from market_site import app, bc, db, TRANSACTIO_ERROR
from market_site.models import Company, HardAsset, User
from flask_login import current_user, login_required

# /user_assets is in the "routest.py" file

@app.route('/market')
@login_required
def market():
	return render_template('market.html', title='Market')

@app.route('/market/stocks')
@login_required
def stocks():
	companies = Company.query.all()
	return render_template('liquid_assets/stocks.html', title='Stocks', companies=companies)

@app.route('/market/stocks/<int:company_id>')
@login_required
def company_stock(company_id):
	company = Company.query.get_or_404(company_id)
	return render_template('liquid_assets/company_stock.html', title='Company stock', company=company)