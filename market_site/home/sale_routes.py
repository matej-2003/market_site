from flask import render_template, request
from market_site import db
from market_site.models import *
from market_site.config import *
from . import home
from flask_login import login_required, current_user
from flask_breadcrumbs import register_breadcrumb


@home.route('/sales')
@login_required
@register_breadcrumb(home, '.home_sales', 'Sales')
def home_sales():
	return render_template('home/sales/sales.html', title='Sales')

@home.route('/sales/asset/h')
@login_required
@register_breadcrumb(home, '.home_sales.home_ha_sales_overview', 'Hard')
def home_ha_sales_overview():
	return render_template('home/sales/ha_sales_overview.html', title='Hard assets sales')

@home.route('/sales/asset/h/sales')
@login_required
@register_breadcrumb(home, '.home_sales.home_ha_sales_overview.home_ha_sales', 'Sale')
def home_ha_sales():
	page = request.args.get('page', 1, type=int)
	sales = db.session.query(HardAssetSale)\
			.where(HardAssetSale.seller_id == current_user.id)\
			.paginate(page=page, per_page=6)
	return render_template('home/sales/ha_sales.html', title='Sales', sales=sales)

@home.route('/sales/asset/h/purchase')
@login_required
@register_breadcrumb(home, '.home_sales.home_ha_sales_overview.home_ha_purchases', 'Purchase')
def home_ha_purchases():
	page = request.args.get('page', 1, type=int)
	sales = db.session.query(HardAssetSale)\
			.where(HardAssetSale.buyer_id == current_user.id)\
			.paginate(page=page, per_page=6)
	return render_template('home/sales/ha_sales.html', title='Purchases', sales=sales, purchase=True)



@home.route('/sales/asset/l')
@login_required
@register_breadcrumb(home, '.home_sales.home_la_sales_overview', 'Liquid')
def home_la_sales_overview():
	return render_template('home/sales/la_sales.html', title='Liquid assets sales')


@home.route('/sales/asset/l/stock')
@login_required
@register_breadcrumb(home, '.home_sales.home_la_sales_overview.home_stock_sales_overview', 'Stock')
def home_stock_sales_overview():
	return render_template('home/sales/stock_sales_overview.html', title='Stock sales')

@home.route('/sales/asset/l/stock/sales')
@login_required
@register_breadcrumb(home, '.home_sales.home_la_sales_overview.home_stock_sales_overview.home_stock_sales', 'Sales')
def home_stock_sales():
	page = request.args.get('page', 1, type=int)
	sales = db.session.query(CompanyShareSale)\
			.where(CompanyShareSale.seller_id == current_user.id)\
			.paginate(page=page, per_page=6)
	return render_template('home/sales/stock_sales.html', title='Stock sales', sales=sales)

@home.route('/sales/asset/l/stock/purchases')
@login_required
@register_breadcrumb(home, '.home_sales.home_la_sales_overview.home_stock_sales_overview.home_stock_purchases', 'Purchases')
def home_stock_purchases():
	page = request.args.get('page', 1, type=int)
	sales = db.session.query(CompanyShareSale)\
			.where(CompanyShareSale.buyer_id == current_user.id)\
			.paginate(page=page, per_page=6)
	return render_template('home/sales/stock_sales.html', title='Stock purchases', sales=sales, purchase=True)




@home.route('/sales/asset/l/bond')
@login_required
@register_breadcrumb(home, '.home_sales.home_la_sales_overview.home_bond_sales_overview', 'bond')
def home_bond_sales_overview():
	return render_template('home/sales/bond_sales_overview.html', title='bond sales')

@home.route('/sales/asset/l/bond/sales')
@login_required
@register_breadcrumb(home, '.home_sales.home_la_sales_overview.home_bond_sales_overview.home_bond_sales', 'Sales')
def home_bond_sales():
	page = request.args.get('page', 1, type=int)
	sales = db.session.query(CompanyBondSale)\
			.where(CompanyBondSale.seller_id == current_user.id)\
			.paginate(page=page, per_page=6)
	return render_template('home/sales/bond_sales.html', title='Bond sales', sales=sales)

@home.route('/sales/asset/l/bond/purchases')
@login_required
@register_breadcrumb(home, '.home_sales.home_la_sales_overview.home_bond_sales_overview.home_bond_purchases', 'Purchases')
def home_bond_purchases():
	page = request.args.get('page', 1, type=int)
	sales = db.session.query(CompanyBondSale)\
			.where(CompanyBondSale.buyer_id == current_user.id)\
			.paginate(page=page, per_page=6)
	return render_template('home/sales/bond_sales.html', title='Bond purchases', sales=sales, purchase=True)

