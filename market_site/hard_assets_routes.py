from crypt import methods
from flask import render_template, redirect, url_for, request, flash
from market_site import app, db, bc, login_manager
from market_site import FOR_SALE, SOLD
from market_site import ART, HISTORICAL_ARTIFACTS, RARE_EARTHS, PRECIOUS_METALS, REAL_ESTATE, OTHER, TRANSPORT
from market_site.models import *
from flask_login import current_user, login_required
from datetime import datetime

# /user_assets is in the "routest.py" file

@app.route('/hard_asset/asset/<int:hard_asset_id>')
@login_required
def hard_asset(hard_asset_id):
	hard_asset = HardAsset.query.get_or_404(hard_asset_id)
	return render_template('hard_assets/asset.html', title='Asset', asset=hard_asset)

@app.route('/hard_asset/asset/<int:hard_asset_id>/sale_history')
@login_required
def hard_asset_sale_history(hard_asset_id):
	hard_asset = HardAsset.query.get_or_404(hard_asset_id)
	return render_template('hard_assets/sale_history.html', title='Sale history', asset=hard_asset, sales=hard_asset.sales)

@app.route('/hard_asset/asset/<int:hard_asset_id>/sale', methods=['GET', 'POST'])
@login_required
def hard_asset_sale(hard_asset_id):
	hard_asset = HardAsset.query.get_or_404(hard_asset_id)
	sale = hard_asset.sales[-1]
	if hard_asset.owner != current_user and hard_asset.is_on_sale():
		if current_user.balance >= sale.price:
			if request.method == 'POST':
				if request.form.get('buy'):
					sale.status = SOLD
					sale.buyer_id = current_user.id
					sale.sale_end = datetime.utcnow()
					current_user.pay(sale.price, hard_asset.owner)
					hard_asset.owner_id = current_user.id
					db.session.commit()
					return redirect(url_for('user_assets'))
		else:
			flash('You do not have enough money')
		return render_template('hard_assets/sale.html', title='Sale', asset=hard_asset, sale=sale)
	else:
		return redirect(url_for('hard_asset', hard_asset_id=hard_asset_id))

@app.route('/hard_asset/asset/<int:hard_asset_id>/sell', methods=['GET', 'POST'])
@login_required
def hard_asset_sell(hard_asset_id):
	hard_asset = HardAsset.query.get_or_404(hard_asset_id)
	sale = hard_asset.sales[-1]
	if hard_asset.owner == current_user:
		if request.method == 'POST':
			try:
				action = request.form.get('action')
				price = float(request.form.get('price'))
				info = request.form.get('info')

				if action and price and info:
					if not hard_asset.is_on_sale():
						hard_asset.info = info.strip(' \n\t')
						has = HardAssetSale(
							price = price,
							hard_asset_id = hard_asset_id,
							seller_id = current_user.id,
						)
						db.session.add(has)
					else:
						if action == "EDIT":
							hard_asset.info = info
							sale.price = price
						elif action == "DELETE":
							db.session.delete(sale)
					db.session.commit()
			except ValueError:
				pass
			return redirect(url_for('user_assets'))
		return render_template('hard_assets/sell.html', title='Sale', asset=hard_asset, sale=sale)
	else:
		return redirect(url_for('hard_asset', hard_asset_id=hard_asset_id))


@app.route('/market/hard_assets')
@login_required
def hard_assets():
	return render_template('hard_assets/index.html', title='Hard asset')

@app.route('/market/hard_assets/<string:category>')
@login_required
def hard_asset_market(category):
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
		.where(HardAssetSale.status == FOR_SALE)\
		.where(HardAsset.type == type).all()
	title = type.lower().replace('_', ' ').capitalize()
	return render_template('hard_assets/real_estate.html', title=title, sales=sales)