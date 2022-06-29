from flask import render_template, request
from market_site import db
from market_site.models import *
from market_site.config import *
from . import home
from flask_login import login_required, current_user
from flask_breadcrumbs import register_breadcrumb


@home.route('/assets')
@login_required
@register_breadcrumb(home, '.home_assets', 'Assets')
def home_assets():
	return render_template('home/assets/assets.html', title='My assets')

@home.route('/assets/h')
@login_required
@register_breadcrumb(home, '.home_assets.home_hard_assets', 'Hard')
def home_hard_assets():
	page = request.args.get('page', 1, type=int)
	hard_assets = db.session.query(HardAsset)\
		.where(HardAsset.owner_id == current_user.id)\
		.paginate(page=page, per_page=6)
	return render_template('home/assets/hard_assets.html', title='Hard assets', hard_assets=hard_assets)

@home.route('/assets/l')
@login_required
@register_breadcrumb(home, '.home_assets.home_liquid_assets', 'Liquid')
def home_liquid_assets():
	return render_template('home/assets/liquid_assets.html', title='Liquid assets')

@home.route('/assets/l/stock')
@login_required
@register_breadcrumb(home, '.home_assets.home_liquid_assets.home_stock', 'Stock')
def home_stock():
	page = request.args.get('page', 1, type=int)
	stock = current_user.shares_().paginate(page=page, per_page=5)
	return render_template('home/assets/stock.html', title='Stock', stock=stock)

@home.route('/assets/l/bonds')
@login_required
@register_breadcrumb(home, '.home_assets.home_liquid_assets.home_bonds', 'Bonds')
def home_bonds():
	page = request.args.get('page', 1, type=int)
	bonds = current_user.bonds_().paginate(page=page, per_page=5)
	return render_template('home/assets/bonds.html', title='Bonds', bonds=bonds)