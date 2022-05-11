from re import S
from market_site import db, FOR_SALE, SOLD, PHYSICAL_PERSON
from market_site.models import *
import random
import datetime

db.create_all()

banks = Bank.query.all()

users = db.session.query(User)\
    .where(User.type == PHYSICAL_PERSON)\
    .all()

for u in users:
    for h in u.hard_assets:
        print(not h.is_under_mortgage()) and (not h.is_on_sale())
        if (not h.is_under_mortgage()) and (not h.is_on_sale()):
            start = datetime.datetime.utcnow()
            auction = Auction(
                hard_asset_id = h.id,
                initial_price = round(h.value * 0.7, 2),
                final_price = round(h.value * 0.7, 2),
                seller_id = u.id,
                bank_id = random.choice(banks).id,
                security_deposit = round(h.value * 0.1, 2),
                start = start,
                end = start + datetime.timedelta(days=2),
            )
            db.session.add(auction)
            print(auction)
            
            for u in users:
                print(u.username, auction.add_bidder(u))
db.session.commit()

auctions = Auction.query.all()
for a in auctions:
    print(a, a.hard_asset.name)
    for b in a.bidders:
        b.place_bid(a.final_price + 10)
        print(a.id, b.user.username, a.bids)