from market_site import db, bc
from market_site.models import *
import json
from sqlalchemy import func, desc

companies = Company.query.all()
users = User.query.all()
hard_assets = HardAsset.query.all()
shares = CompanyShare.query.all()
auction = Auction.query.all()
auction_bidders = AuctionBidder.query.all()
auction_bids = AuctionBid.query.all()

c  = companies[0]
u  = users[0]
h  = hard_assets[0]
cs = shares[0]

# print(json.dumps(c))

# db.session.query(CompanyShare)\
#     .filter_by()

# q = db.session.query(
#         func.count(CompanyShareSale.price).label('share_number'),
#         CompanyShareSale,
#         CompanyShare,
#         Company,
#         User,
#     )\
#     .join(CompanyShare, CompanyShareSale.share_id == CompanyShare.id)\
#     .join(Company, CompanyShare.company_id == Company.id)\
#     .join(User, CompanyShare.owner_id == User.id)\
#     .where(Company.id == 1)\
#     .group_by(Company.id, User.id, CompanyShareSale.price)\
#     .order_by(desc('share_number'))
# print(q.all())

# for i in q.all():
#     print(i)

# q = db.session.query(
#         Company.name,
#         User.username,
#         CompanyShareSale.price,
#         CompanyShareSale.sale_end,
#     )\
#     .join(CompanyShare, CompanyShareSale.share_id == CompanyShare.id)\
#     .join(Company, CompanyShare.company_id == Company.id)\
#     .join(User, CompanyShare.owner_id == User.id)\
#     .where(Company.id == 1, CompanyShareSale.status == SOLD)\

# data = []

# for c, u, p, t in q.all():
#     data.append([
#         t.strftime("%d/%m/%Y %H:%M:%S"),
#         p
#     ])
#     print(f'{c} -> {u} [{t.strftime("%d/%m/%Y %H:%M:%S")}]: ${p}')

# print(json.dumps(data))

# select company_bond_sales, users, companies, company_bonds, count(company_bond_sales.price)
# from company_bond_sales
# inner join company_bonds on company_bond_sales.bond_id = company_bonds.id
# inner join companies on company_bonds.company_id = companies.id
# inner join users on company_bond_sales.seller_id = users.id
# where companies.id = 6 and company_bond_sales.status = 0
# group by users.username, company_bonds.value, company_bonds.interest_rate, company_bond_sales.price
# order by users.username, company_bonds.value, company_bonds.interest_rate, company_bond_sales.price

# q = db.session.query(
#         CompanyBondSale.id,
#         User.username,
#         CompanyBond.value, 
#         CompanyBond.interest_rate,
#         CompanyBondSale.price,
#         func.count(CompanyBondSale.price).label('number'),
#     )\
#     .join(CompanyBond, CompanyBondSale.bond_id == CompanyBond.id)\
#     .join(User, CompanyBond.owner_id == User.id)\
#     .where(CompanyBond.company_id == 6, CompanyBondSale.status == FOR_SALE)\
#     .group_by(CompanyBond.owner_id, CompanyBond.value, CompanyBond.interest_rate, CompanyBondSale.price)\
#     .order_by(CompanyBond.owner_id, CompanyBond.value, CompanyBond.interest_rate, CompanyBondSale.price)
    # .order_by(desc('share_number'))

# for i in q.all():
#     print(i)