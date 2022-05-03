from market_site import db, bc
from market_site.models import *
import json
from sqlalchemy import func, desc

companies = Company.query.all()
users = User.query.all()
hard_assets = HardAsset.query.all()
shares = CompanyShare.query.all()

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

q = db.session.query(
        Company.name,
        User.username,
        CompanyShareSale.price,
        CompanyShareSale.sale_end,
    )\
    .join(CompanyShare, CompanyShareSale.share_id == CompanyShare.id)\
    .join(Company, CompanyShare.company_id == Company.id)\
    .join(User, CompanyShare.owner_id == User.id)\
    .where(Company.id == 1, CompanyShareSale.status == SOLD)\

data = []

for c, u, p, t in q.all():
    data.append([
        t.strftime("%d/%m/%Y %H:%M:%S"),
        p
    ])
    print(f'{c} -> {u} [{t.strftime("%d/%m/%Y %H:%M:%S")}]: ${p}')

print(json.dumps(data))