from flask import render_template, Blueprint
from market_site import db
from market_site.config import *
from market_site.models import *
from flask_login import login_required
from sqlalchemy import func, desc

liquid_assets = Blueprint("liquid_assets", __name__)

@liquid_assets.route('/asset/l')
@login_required
def list_liquid_assets():
	shares = CompanyShareSale.query.all()
	bonds = CompanyBondSale.query.all()
	return render_template('hard_assets/asset.html', title='Asset', shares=shares, bonds=bonds)


@liquid_assets.route('/assets/l/company/<int:company_id>')
@login_required
def company(company_id):
	company = Company.query.get_or_404(company_id)
	return render_template('/assets/liquid/company.html', title='Company', company=company)



@liquid_assets.route('/assets/l/company/<int:company_id>/stock')
@login_required
def company_stock(company_id):
	company = Company.query.get_or_404(company_id)
	q = db.session.query(func.count(CompanyShare.company_id).label('share_number'), User)\
		.join(User, CompanyShare.owner_id == User.id)\
		.where(CompanyShare.company_id == company.id)\
		.group_by(CompanyShare.owner_id)\
		.order_by(desc('share_number'))
	return render_template('/assets/liquid/company_stock_info.html', title='Company stock', company=company, shares=q.all())



@liquid_assets.route('/assets/l/company/<int:company_id>/bonds')
@login_required
def company_bonds(company_id):
	company = Company.query.get_or_404(company_id)
	q = db.session.query(func.count(CompanyBond.company_id).label('share_number'), User, CompanyBond)\
		.join(User, CompanyBond.owner_id == User.id)\
		.where(CompanyBond.company_id == company.id)\
		.group_by(CompanyBond.owner_id, CompanyBond.value, CompanyBond.interest_rate)\
		.order_by(desc('share_number'))
	print(q.all())
	return render_template('/assets/liquid/company_bond_info.html', title='Company Bonds', company=company, bonds=q.all())