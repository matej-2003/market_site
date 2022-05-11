from flask import render_template, url_for, flash, redirect, request, abort
from market_site import app, bc, db, FOR_SALE
from market_site.models import HardAsset, Auction
from flask_login import current_user, login_required

# /user_assets is in the "routest.py" file

@app.route('/market')
@login_required
def market():
	return render_template('market.html', title='Market')


@app.route('/market/auctions')
@login_required
def auctions():
	auctions = db.session.query(Auction).where(Auction.status == FOR_SALE, Auction.seller_id != current_user.id).all()
	return render_template('auction/auctions.html', title='Auctions', auctions=auctions)


@app.route('/market/auction/<int:auction_id>/join', methods=['GET', 'POST'])
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


@app.route('/market/auction/<int:auction_id>', methods=['GET', 'POST'])
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
				flash('error')
		return render_template('auction/auction.html', title='Auction', auction=auction)
	return redirect(url_for('join_auction', auction_id=auction_id))