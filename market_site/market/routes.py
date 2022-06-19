from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from market_site import bc, db
from market_site.models import *
from market_site.config import *
from flask_login import current_user, login_required

# /user_assets is in the "routest.py" file
market = Blueprint("market", __name__)

@market.route('/market')
@login_required
def market_():
	return render_template('market.html', title='Market')


@market.route('/market/auctions')
@login_required
def auctions():
	auctions = db.session.query(Auction).where(Auction.status == FOR_SALE, Auction.seller_id != current_user.id).all()
	return render_template('auction/auctions.html', title='Auctions', auctions=auctions)


@market.route('/market/auction/<int:auction_id>', methods=['GET', 'POST'])
@login_required
def auction(auction_id):
	auction = Auction.query.get_or_404(auction_id)
	if auction.is_bidder(current_user):
		if request.method == 'POST':
			bid_amount = float(request.form.get('bid_amount'))
			bid_submit = request.form.get('bid_submit')
			auction_unjoin = request.form.get('auction_unjoin')
			print(bid_amount, bid_submit, auction_unjoin)
			try:
				bid_amount = float(bid_amount)
				if bid_amount and bid_submit:
					if bid_amount > auction.final_price:
						auction.place_bid(current_user, bid_amount)
				if auction_unjoin:
					auction.remove_bidder(current_user)
					return redirect(url_for('join_auction', auction_id=auction_id))
			except ValueError:
				flash('error', 'error')
		return render_template('auction/auction.html', title='Auction', auction=auction)
	return redirect(url_for('join_auction', auction_id=auction_id))


@market.route('/market/auction/<int:auction_id>/join', methods=['GET', 'POST'])
@login_required
def join_auction(auction_id):
	auction = Auction.query.get_or_404(auction_id)
	if request.method == 'POST':
		agree_to_terms = request.form.get('agree_to_terms')
		agree_to_commission = request.form.get('agree_to_commission')
		if agree_to_terms and agree_to_commission:
			auction.add_bidder(current_user)
		return redirect(url_for('auction', auction_id=auction_id))
	return render_template('auction/join_auction.html', title='Auction', auction=auction)


@market.route('/market/auction/<int:auction_id>/history', methods=['GET', 'POST'])
@login_required
def auction_history(auction_id):
	auction = Auction.query.get_or_404(auction_id)
	return render_template('auction/history.html', title='Auction', auction=auction)









@market.route('/market/assets/h')
@login_required
def market_hard_assets():
	return render_template('hard_assets/index.html', title='Hard asset')

@market.route('/market/assets/h/<string:category>')
@login_required
def market_hard_asset_category(category):
	category = category.upper()
	type = OTHER
	if category == REAL_ESTATE:
		type = REAL_ESTATE
	elif category == ART:
		type = ART
	elif category == HISTORICAL_ARTIFACTS:
		type = HISTORICAL_ARTIFACTS
	elif category == RARE_EARTHS:
		type = RARE_EARTHS
	elif category == PRECIOUS_METALS:
		type = PRECIOUS_METALS
	elif category == TRANSPORT:
		type = TRANSPORT
	elif category == OTHER:
		type = OTHER

	# sales = HardAssetSale.query.filter_by(status=FOR_SALE, hard_asset.type=type).all()
	sales = db.session.query(HardAssetSale)\
		.join(HardAsset, HardAssetSale.hard_asset_id==HardAsset.id)\
		.where(HardAssetSale.status == FOR_SALE, HardAsset.type == type).all()
	title = type.lower().replace('_', ' ').capitalize()
	return render_template('assets/hard/market.html', title=title, sales=sales)








@market.route('/market/liquid_assets')
@login_required
def market_liquid_assets():
	return render_template('liquid_assets/index.html', title='Liquid asset')



@market.route('/market/liquid_assets/bonds')
@login_required
def market_bonds():
	companies = Company.query.all()
	return render_template('liquid_assets/bond_market.html', title='Bond market', companies=companies)



@market.route('/market/liquid_assets/stocks')
@login_required
def market_stocks():
	companies = Company.query.all()
	return render_template('liquid_assets/stock_market.html', title='Stock market', companies=companies)



@market.route('/market/liquid_assets/stocks/<int:company_id>/sell', methods = ['GET', 'POST'])
@login_required
def market_sell_stock(company_id):
	company = Company.query.get_or_404(company_id)
	user_share_number = current_user.share_number(company)
	if request.method == 'POST':
		share_number = request.form.get('share_number')
		price = request.form.get('price')
		try:
			share_number = float(share_number)
			price = float(price)
			if share_number <= user_share_number and price >= 0:

				for i, s in enumerate(current_user.get_shares(company)):
					if i < share_number:
						ss = CompanyShareSale(
							price = price,
							status = FOR_SALE,
							share_id = s.id,
							seller_id = current_user.id,
						)
						db.session.add(ss)
						db.session.commit()
		except ValueError:
			flash('value error', 'error')
	return render_template('liquid_assets/company_stock_sell.html', title='Company stock market', company=company, user_share_number=current_user.share_number(company))



@market.route('/market/liquid_assets/bonds/<int:company_id>/sell', methods = ['GET', 'POST'])
@login_required
def market_sell_bond(company_id):
	company = Company.query.get_or_404(company_id)
	user_bond_number = current_user.bond_number(company)
	if request.method == 'POST':
		bond_number = request.form.get('bond_number')
		price = request.form.get('price')
		try:
			bond_number = float(bond_number)
			price = float(price)
			if bond_number <= user_bond_number and price >= 0:

				for i, s in enumerate(current_user.get_bonds(company)):
					if i < bond_number:
						ss = CompanyBondSale(
							price = price,
							status = FOR_SALE,
							bond_id = s.id,
							seller_id = current_user.id,
						)
						db.session.add(ss)
						db.session.commit()
			else:
				flash('You canot sell bonds you don\'t have', 'error')
		except ValueError:
			flash('value error', 'error')
	return render_template('liquid_assets/company_bond_sell.html', title='Company bond market', company=company, user_bond_number=current_user.bond_number(company))




@market.route('/market/liquid_assets/stocks/<int:company_id>', methods = ['GET', 'POST'])
@login_required
def stock_market(company_id):
	company = Company.query.get_or_404(company_id)
	# share_sales = db.session.query(CompanyShareSale).where(CompanyShareSale.status == FOR_SALE).all()
	share_sales = db.session.query(
			func.count(CompanyShareSale.price).label('share_number'),
			CompanyShareSale,
			CompanyShare,
			Company,
			User,
		)\
		.join(CompanyShare, CompanyShareSale.share_id == CompanyShare.id)\
		.join(Company, CompanyShare.company_id == Company.id)\
		.join(User, CompanyShare.owner_id == User.id)\
		.where(Company.id == company_id, CompanyShareSale.status == FOR_SALE)\
		.group_by(User.id, CompanyShareSale.price)\
		.order_by(desc('share_number'))
	return render_template('liquid_assets/company_stock_market.html', title='Company stock market', company=company, share_sales=share_sales.all())



@market.route('/market/liquid_assets/bonds/<int:company_id>', methods = ['GET', 'POST'])
@login_required
def bond_market(company_id):
	company = Company.query.get_or_404(company_id)
	bond_sales = db.session.query(
		func.count(CompanyBondSale.price).label('number'),
		CompanyBondSale,
		CompanyBond,
		User,
	)\
	.join(CompanyBond, CompanyBondSale.bond_id == CompanyBond.id)\
	.join(User, CompanyBond.owner_id == User.id)\
	.where(CompanyBond.company_id == 6, CompanyBondSale.status == FOR_SALE)\
	.group_by(CompanyBond.owner_id, CompanyBond.value, CompanyBond.interest_rate, CompanyBondSale.price)\
	.order_by(CompanyBond.owner_id, CompanyBond.value, CompanyBond.interest_rate, CompanyBondSale.price)
	return render_template('liquid_assets/company_bond_market.html', title='Company bond market', company=company, bond_sales=bond_sales.all())
