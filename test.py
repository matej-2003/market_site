from market_site import db, bc
from market_site.models import *

companies = Company.query.all()
users = User.query.all()
hard_assets = HardAsset.query.all()
shares = CompanyShare.query.all()

c  = companies[0]
u  = users[0]
h  = hard_assets[0]
cs = shares[0]

# db.session.query(CompanyShare)\
#     .filter_by()