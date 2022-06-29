from flask import render_template, Blueprint, request
from market_site import db
from market_site.models import *
from market_site.config import *
from . import home
from flask_login import login_required, current_user
from flask_breadcrumbs import register_breadcrumb
from sqlalchemy import or_



@home.route('/auctions')
@login_required
@register_breadcrumb(home, '.home_auctions', 'Auctions')
def home_auctions():
	auctions = db.session.query(Auction)\
		.where(Auction.seller_id == current_user.id).all()
	return render_template('home/auctions/auctions.html', title='Auctions', auctions=auctions)



@home.route('/auctions/sale')
@login_required
@register_breadcrumb(home, '.home_auctions.home_sale_auctions', 'Sales')
def home_sale_auctions():
	return render_template('home/auctions/sales_auction.html', title='Sales auctions')


@home.route('/auctions/sale/active')
@login_required
@register_breadcrumb(home, '.home_auctions.home_sale_auctions.home_sale_auctions_active', 'Active')
def home_sale_auctions_active():
	auctions = db.session.query(Auction)\
		.where(Auction.seller_id == current_user.id)\
		.where(Auction.is_over(Auction) == False).all()
	return render_template('home/auctions/sales_auctions.html', title='Active sales auctions', auctions=auctions)

@home.route('/auctions/sale/finnished')
@login_required
@register_breadcrumb(home, '.home_auctions.home_sale_auctions.home_sale_auctions_finnished', 'Finnished')
def home_sale_auctions_finnished():
	auctions = db.session.query(Auction)\
		.where(Auction.seller_id == current_user.id)\
		.where(Auction.is_over(Auction) == True).all()
	return render_template('home/auctions/sales_auctions.html', title='Finnished sales auctions', auctions=auctions)


@home.route('/auctions/purchase')
@login_required
@register_breadcrumb(home, '.home_auctions.home_purchase_auctions', 'Purchases')
def home_purchase_auctions():
	return render_template('home/auctions/purchase_auction.html', title='Purchases auctions')


@home.route('/auctions/purchase/active')
@login_required
@register_breadcrumb(home, '.home_auctions.home_purchase_auctions.home_purchase_auctions_active', 'Active')
def home_purchase_auctions_active():
	auctions = db.session.query(Auction)\
		.where(Auction.buyer_id == current_user.id)\
		.where(Auction.is_over(Auction) == False).all()
	return render_template('home/auctions/purchase_auctions.html', title='Active purchase auctions', auctions=auctions)

@home.route('/auctions/purchase/finnished')
@login_required
@register_breadcrumb(home, '.home_auctions.home_purchase_auctions.home_purchase_auctions_finnished', 'Finnished')
def home_purchases_auctions_finnished():
	auctions = db.session.query(Auction)\
		.where(Auction.buyer_id == current_user.id)\
		.where(Auction.is_over(Auction) == True).all()
	return render_template('home/auctions/purchase_auctions.html', title='Finnished purchase auctions', auctions=auctions)
