from flask import render_template, url_for, flash, redirect, request, abort
from market_site import app, bc, db, TRANSACTIO_ERROR
from market_site.forms import LoginForm
from market_site.models import User, Company
from flask_login import current_user, login_required

# /user_assets is in the "routest.py" file

@app.route('/liquid_assets/company/<int:company_id>')
@login_required
def company(company_id):
	company = Company.query.get_or_404(company_id)
	return render_template('liquid_assets/company.html', title='Company', company=company)

@app.route('/market/liquid_assets')
@login_required
def liquid_assets():
	return render_template('liquid_assets/index.html', title='Liquid asset')