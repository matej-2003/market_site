from flask import render_template, url_for, flash, redirect, request, abort
from market_site import app, bc, db, TRANSACTIO_ERROR
from market_site.models import Company, HardAsset, User
from flask_login import current_user, login_required

# /user_assets is in the "routest.py" file

@app.route('/market')
@login_required
def market():
	return render_template('market.html', title='Market')
