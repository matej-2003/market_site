from flask import render_template, redirect, url_for, request, flash, Blueprint
from market_site import db
from market_site.config import *
from market_site.models import *
from flask_login import current_user, login_required
from datetime import datetime

hard_assets = Blueprint("hard_assets", __name__, url_prefix="/asset/h", template_folder="templates")

# /user_assets is in the "routest.py" file
@hard_assets.route('/list')
@login_required
def list_hard_assets():
	assets = HardAsset.query.all()
	return render_template('assets/hard/asset.html', title='Asset', assets=assets)



@hard_assets.route('/<int:ha_id>')
@login_required
def hard_asset(ha_id):
	hard_asset = HardAsset.query.get_or_404(ha_id)
	return render_template('assets/hard/asset.html', title='Asset', asset=hard_asset)



@hard_assets.route('/<int:ha_id>/sale', methods=['GET', 'POST'])
@login_required
def ha_sale(ha_id):
	hard_asset = HardAsset.query.get_or_404(ha_id)
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
					flash(f'You have succesfully bought <a href="/asset/h/{hard_asset.id}">{hard_asset.name}</a>', 'success')
					return redirect(url_for('user_assets'))
		else:
			flash('You do not have enough money', 'success')
		return render_template('assets/hard/sale.html', title='Sale', asset=hard_asset, sale=sale)
	else:
		return redirect(url_for('hard_asset', ha_id=ha_id))


@hard_assets.route('/<int:ha_id>/sale/create')
@login_required
def ha_sale_create(ha_id):
	hard_asset = HardAsset.query.get_or_404(ha_id)
	return redirect(url_for('sale_create', sale_id=hard_asset.last_sale()))


@hard_assets.route('/<int:ha_id>/sale/delete')
@login_required
def ha_sale_delete(ha_id):
	hard_asset = HardAsset.query.get_or_404(ha_id)
	return redirect(url_for('sale_delete', sale_id=hard_asset.last_sale()))


@hard_assets.route('/<int:ha_id>/sale/edit')
@login_required
def ha_sale_edit(ha_id):
	hard_asset = HardAsset.query.get_or_404(ha_id)
	return redirect(url_for('sale_edit', sale_id=hard_asset.last_sale()))


@hard_assets.route('/<int:ha_id>/sale/history')
@login_required
def ha_sale_history(ha_id):
	asset = HardAsset.query.get_or_404(ha_id)
	sales = db.session.query(HardAssetSale)\
			.where(HardAssetSale.hard_asset_id == ha_id).all()
	return render_template('assets/hard/sale_history.html', sales=sales, asset=asset)




@hard_assets.route('/<int:ha_id>/auction/create')
@login_required
def ha_auction_create(ha_id):
	hard_asset = HardAsset.query.get_or_404(ha_id)
	return redirect(url_for('auction_create', auction_id=hard_asset.last_auction()))


@hard_assets.route('/<int:ha_id>/auction/delete')
@login_required
def ha_auction_delete(ha_id):
	hard_asset = HardAsset.query.get_or_404(ha_id)
	return redirect(url_for('auction_delete', auction_id=hard_asset.last_auction()))


@hard_assets.route('/<int:ha_id>/auction/edit')
@login_required
def ha_auction_edit(ha_id):
	hard_asset = HardAsset.query.get_or_404(ha_id)
	return redirect(url_for('auction_edit', auction_id=hard_asset.last_auction()))


@hard_assets.route('/<int:ha_id>/auction/history')
@login_required
def ha_auction_history(ha_id):
	hard_asset = HardAsset.query.get_or_404(ha_id)
	return redirect(url_for('auction_history', auction_id=hard_asset.last_auction()))


@hard_assets.route('/<int:ha_id>/sell', methods=['GET', 'POST'])
@login_required
def ha_sell(ha_id):
	hard_asset = HardAsset.query.get_or_404(ha_id)
	sale = None
	if len(hard_asset.sales) > 0:
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
							hard_asset_id = ha_id,
							seller_id = current_user.id,
						)
						db.session.add(has)
					else:
						if action == "CONFIRM":
							hard_asset.info = info
							sale.price = price
						elif action == "DELETE":
							db.session.delete(sale)
					db.session.commit()
			except ValueError:
				pass
			return redirect(url_for('home.home_hard_assets'))
		return render_template('assets/hard/sell.html', title='Sall', asset=hard_asset, sale=sale)
	return redirect(url_for('hard_asset', ha_id=ha_id))


@hard_assets.route('/<int:ha_id>/auction', methods=['GET', 'POST'])
@login_required
def ha_auction(ha_id):
	hard_asset = HardAsset.query.get_or_404(ha_id)
	if hard_asset.owner == current_user:
		return render_template('assets/hard/auction.html', title='Sall', asset=hard_asset)
	return redirect(url_for('hard_asset', ha_id=ha_id))
