from flask import render_template
from market_site import db
from market_site.models import *
from market_site.config import *
from . import home
from flask_login import login_required, current_user
from flask_breadcrumbs import register_breadcrumb
from sqlalchemy import or_


@home.route('/sales')
@login_required
@register_breadcrumb(home, '.home_sales', 'Sales')
def home_sales():
	return render_template('home/sales/sales.html', title='Sales')

@home.route('/sales/asset/h')
@login_required
@register_breadcrumb(home, '.home_sales.home_hsales', 'Hard')
def home_hsales():
	sales = db.session.query(HardAssetSale)\
			.where(HardAssetSale.seller_id == current_user.id).all()
	purchases = db.session.query(HardAssetSale)\
			.where(HardAssetSale.buyer_id == current_user.id).all()
	return render_template('home/sales/hard_assets_sales.html', title='Hard assets sales', sales=sales, purchases=purchases)

@home.route('/sales/asset/l')
@login_required
@register_breadcrumb(home, '.home_sales.home_lsales', 'Liquid')
def home_lsales():
	return render_template('home/sales/liquid_assets_sales.html', title='Liquid assets sales')


@home.route('/sales/asset/l/stock')
@login_required
@register_breadcrumb(home, '.home_sales.home_lsales.home_stock_sales', 'Stock')
def home_stock_sales():
	sales = db.session.query(CompanyShareSale)\
			.where(CompanyShareSale.seller_id == current_user.id).all()
	purchases = db.session.query(CompanyShareSale)\
			.where(CompanyShareSale.buyer_id == current_user.id).all()
	return render_template('home/sales/stock_sales.html', title='Stock sales', sales=sales, purchases=purchases)


@home.route('/sales/asset/l/bond')
@login_required
@register_breadcrumb(home, '.home_sales.home_lsales.home_bond_sales', 'Bond')
def home_bond_sales():
	sales = db.session.query(CompanyBondSale)\
			.where(CompanyBondSale.seller_id == current_user.id).all()
	purchases = db.session.query(CompanyBondSale)\
			.where(CompanyBondSale.buyer_id == current_user.id).all()
	return render_template('home/sales/bond_sales.html', title='Bond sales', sales=sales, purchases=purchases)