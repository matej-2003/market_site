from flask import Response, Blueprint
from market_site.config import SOLD
from market_site.models import *
from flask_login import login_required
import json

api = Blueprint("api", __name__)

@api.route('/api/user/<int:user_id>/hard_assets')
@login_required
def api_user_hard_assets(user_id):
	user = User.query.get_or_404(user_id)
	data = []
	for hard_asset in user.hard_assets:
		data.append(hard_asset.objectify())
	return Response(json.dumps(data), mimetype='text/json')



@api.route('/api/company/<int:company_id>/stocks')
@login_required
def company_stock_data(company_id):
	q = db.session.query(
			CompanyShareSale.price,
			CompanyShareSale.end,
		)\
		.join(CompanyShare, CompanyShareSale.share_id == CompanyShare.id)\
		.join(Company, CompanyShare.company_id == Company.id)\
		.join(User, CompanyShare.owner_id == User.id)\
		.where(Company.id == company_id, CompanyShareSale.status == SOLD)
	data = []
	for p, t in q.all():
		# data.append([p, t.strftime("%d/%m/%Y %H:%M:%S")])
		data.append([p, t.strftime("%d/%m/%Y %H:%M:%S")])

	return Response(json.dumps(data), mimetype='text/json')



@api.route('/api/company/<int:company_id>/bonds')
@login_required
def company_bond_data(company_id):
	q = db.session.query(
			CompanyBondSale.price,
			CompanyBondSale.end,
		)\
		.join(CompanyBond, CompanyBondSale.bond_id == CompanyBond.id)\
		.join(Company, CompanyBond.company_id == Company.id)\
		.join(User, CompanyBond.owner_id == User.id)\
		.where(Company.id == company_id, CompanyBondSale.status == SOLD)

	data = []
	for p, t in q.all():
		# data.append([p, t.strftime("%d/%m/%Y %H:%M:%S")])
		data.append([p, t.strftime("%d/%m/%Y %H:%M:%S")])

	return Response(json.dumps(data), mimetype='text/json')