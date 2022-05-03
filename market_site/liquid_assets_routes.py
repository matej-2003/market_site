from flask import render_template, url_for, flash, redirect, request, abort, Response
from market_site import FOR_SALE, app, bc, db, TRANSACTIO_ERROR, SOLD
from market_site.forms import LoginForm
from market_site.models import CompanyShareSale, User, Company, CompanyShare, CompanyBond
from flask_login import current_user, login_required
from sqlalchemy import func, desc
import json

@app.route('/liquid_assets/company/<int:company_id>')
@login_required
def company(company_id):
	company = Company.query.get_or_404(company_id)
	return render_template('liquid_assets/company.html', title='Company', company=company)

@app.route('/liquid_assets/company/<int:company_id>/stock')
@login_required
def company_stock(company_id):
	company = Company.query.get_or_404(company_id)
	q = db.session.query(func.count(CompanyShare.company_id).label('share_number'), User)\
		.join(User, CompanyShare.owner_id == User.id)\
		.where(CompanyShare.company_id == company.id)\
		.group_by(CompanyShare.company_id)\
		.group_by(CompanyShare.owner_id)\
		.order_by(desc('share_number'))
	return render_template('liquid_assets/company_stock_info.html', title='Company stock', company=company, shares=q.all())

@app.route('/liquid_assets/company/<int:company_id>/bonds')
@login_required
def company_bonds(company_id):
	company = Company.query.get_or_404(company_id)
	q = db.session.query(func.count(CompanyBond.company_id).label('share_number'), User, CompanyBond)\
		.join(User, CompanyBond.owner_id == User.id)\
		.where(CompanyBond.company_id == company.id)\
		.group_by(CompanyBond.company_id)\
		.group_by(CompanyBond.owner_id)\
		.order_by(desc('share_number'))
	print(q.all())
	return render_template('liquid_assets/company_bonds.html', title='Company Bonds', company=company, bonds=q.all())


# market

@app.route('/market/liquid_assets')
@login_required
def liquid_assets():
	return render_template('liquid_assets/index.html', title='Liquid asset')

@app.route('/market/liquid_assets/stocks')
@login_required
def stocks():
	companies = Company.query.all()
	return render_template('liquid_assets/stock_market.html', title='Stock market', companies=companies)

@app.route('/market/liquid_assets/stocks/<int:company_id>/sell', methods = ['GET', 'POST'])
@login_required
def sell_stock(company_id):
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
			flash('value error')
	return render_template('liquid_assets/company_stock_sell.html', title='Company stock market', company=company, user_share_number=current_user.share_number(company))

@app.route('/market/liquid_assets/stocks/<int:company_id>', methods = ['GET', 'POST'])
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
		.where(Company.id == 1)\
		.group_by(Company.id, User.id, CompanyShareSale.price)\
		.order_by(desc('share_number'))
	return render_template('liquid_assets/company_stock_market.html', title='Company stock market', company=company, share_sales=share_sales.all())



@app.route('/api/company/<int:company_id>/stocks')
@login_required
def company_stock_data(company_id):
	q = db.session.query(
			CompanyShareSale.price,
			CompanyShareSale.sale_end,
		)\
		.join(CompanyShare, CompanyShareSale.share_id == CompanyShare.id)\
		.join(Company, CompanyShare.company_id == Company.id)\
		.join(User, CompanyShare.owner_id == User.id)\
		.where(Company.id == company_id, CompanyShareSale.status == SOLD)
	data = []
	for p, t in q.all():
		data.append([p, t.strftime("%d/%m/%Y %H:%M:%S")])

	return Response(json.dumps(data), mimetype='text/json')