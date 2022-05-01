from datetime import datetime
from email.mime import image
from market_site import FOR_SALE, OTHER, SOLD, db, bc, login_manager, TRANSACTIO_ERROR, TRANSACTIO_OK, LEGAL_PERSON, PHYSICAL_PERSON, OK, ERROR
from sqlalchemy import func
from flask_login import UserMixin
import json
import random
import os

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=True)
    full_name = db.Column(db.String(80), unique=False, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    type = db.Column(db.Integer, default=PHYSICAL_PERSON)
    # company = db.Column(db.String(40), unique=True, nullable=True)      # only if the type==LEGAL_PERSON
    company_id = db.Column(db.Integer, unique=True, nullable=True)      # only if the type==LEGAL_PERSON

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    balance = db.Column(db.Float, nullable=False, default=0)
    hard_assets = db.relationship('HardAsset', backref='owner', lazy=True)
    company_shares = db.relationship('CompanyShare', backref='owner', lazy=True)
    total_payments_received = db.Column(db.Float, nullable=True, default=0)
    total_payments_made = db.Column(db.Float, nullable=True, default=0)

    def share_number(self, company):
        return len(db.session.query(CompanyShare).filter_by(company_id=company.id, owner_id=self.id).all())

    def share_value(self, company):
        n = len(company.shares)
        if n > 0:
            return self.share_number(company) * (company.value / len(company.shares))
        return 0
    
    def share_percentage(self, company):
        n = company.share_number()
        if n > 0:
            return self.share_number(company) / company.share_number()
        return 0

    def shares(self):
        q = db.session.query(Company, func.count(CompanyShare.company_id).label('share_number'))\
            .join(User, CompanyShare.owner_id==User.id)\
            .join(Company, CompanyShare.company_id==Company.id)\
            .where(User.id == self.id)\
            .group_by(Company.name)\
            .order_by('share_number')
        return q.all()

    def payments_received(self):
        return Transaction.query.filter_by(payee_id=self.id).all()
    
    def payments_made(self):
        return Transaction.query.filter_by(payer_id=self.id).all()

    def pay(self, amount, payee, info=None):
        if (amount <= self.balance) and (amount > 0) and (self.id != payee.id):
            self.balance -= amount
            payee.receive_payment(amount)
            payee.total_payments_received += amount
            self.total_payments_made += amount
            t = Transaction(payer_id=self.id, payee_id=payee.id, amount=amount, info=info)
            db.session.add(t)
            db.session.commit()
            return TRANSACTIO_OK
        else:
            return TRANSACTIO_ERROR
    
    def receive_payment(self, amount):
        self.balance += amount
    
    def get_company(self):
        return Company.query.get(self.company_id)

    def __repr__(self):
        return f'User({self.id}, {self.username}, {self.email})'


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    payer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    payer = db.relationship("User", foreign_keys=[payer_id])
    payee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    payee = db.relationship("User", foreign_keys=[payee_id])
    amount = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    info = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'HardAsset({self.time}, ${self.amount}, {self.payer.username} -> {self.payee.username}, {self.id})'


class HardAsset(db.Model):
    __tablename__ = 'hard_assets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    value = db.Column(db.Float, nullable=False, default=0)
    info = db.Column(db.Text, nullable=True)
    images = db.Column(db.Text, nullable=True)
    amount = db.Column(db.Float, nullable=False, default=1)
    type = db.Column(db.String(50), nullable=True, default=OTHER)
    # mortgage_status = db.Column(db.Integer, nullable=False, default=FOR_SALE)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    sales = db.relationship('HardAssetSale', backref='hard_asset', lazy=True)

    # owner1 = db.relationship("User", foreign_keys=[owner_id])

    def is_on_sale(self):
        if not self.sales:
            return False
        elif self.sales[-1].status == SOLD:
            return False
        else:
            return True

    def get_images(self):
        image_list = []
        try:
            image_list = json.loads(self.images)
            return image_list
        except:
            return False

    def __repr__(self):
        return f'HardAsset({self.id}, name={self.name}, value={self.value}, owner={self.owner})'


class HardAssetSale(db.Model):
    __tablename__ = 'hard_asset_sales'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False, default=0)
    status = db.Column(db.Integer, nullable=False, default=FOR_SALE)
    hard_asset_id = db.Column(db.Integer, db.ForeignKey('hard_assets.id'))
    seller_id = db.Column(db.Integer, nullable=True)
    buyer_id = db.Column(db.Integer, nullable=True)

    sale_start = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    sale_end = db.Column(db.DateTime, nullable=True)

    def sell(self, buyer):
        if buyer.balance >= self.price and buyer != self.hard_asset.owner:
            buyer.pay(self.price, self.hard_asset.owner, info=f"{self}")
            self.buyer_id = buyer.id
            self.hard_asset.owner_id = buyer.id
            self.status = SOLD
            self.sale_end = datetime.utcnow()
            db.session.commit()
            return OK
        return ERROR
    
    def get_buyer(self):
        return User.query.get(self.buyer_id)

    def get_seller(self):
        return User.query.get(self.seller_id)

    def __repr__(self):
        return f'HardAssetSale({self.id}, name={self.hard_asset.name}, price={self.price})'


class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    value = db.Column(db.Float, nullable=False, default=0)
    info = db.Column(db.Text, nullable=True)
    images = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(50), nullable=True)
    shares = db.relationship('CompanyShare', backref='company', lazy=True)
    legal_person_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    legal_person = db.relationship("User", foreign_keys=[legal_person_id])

    # def __init__(self, *args, **kvargs):
    #     super().__init__(*args, **kvargs)
    #     self.init_on_load()

    # @reconstructor
    # def init_on_load(self):
    #     self.id = random.randint(0, 100000000)
    #     self.legal_person = User(
    #         username = str(self.id),
    #         password = bc.generate_password_hash(str(self.id)),
    #         type = LEGAL_PERSON,
    #         company_id = self.id,
    #         balance = 0,
    #     )
    #     self.legal_person_id = self.legal_person.id
    #     db.session.add(self.legal_person)
    #     db.session.commit()

    # def holding(self, company):
    #     for i in self.shares:
    #         if i.company_id == company.id:
    #             return True
    #         else:
    #             return 


    # def subsidiary(self, company):
    #     pass

    def share_number(self):
        return len(self.shares)
    
    def share_value(self):
        n = self.share_number()
        if n > 0:
            return self.value / self.share_number()
        return 0

    def get_images(self):
        image_list = []
        try:
            image_list = json.loads(self.images)
            return image_list
        except:
            return False

    def __repr__(self):
        return f'Company({self.id}, {self.name}, value={self.value})'


class CompanyShare(db.Model):
    __tablename__ = 'company_shares'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'CompanyShare({self.id}, company={self.company_id}, owner={self.owner_id})'