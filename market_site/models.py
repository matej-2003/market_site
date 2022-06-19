import json
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import desc, func

from market_site import bc, db, login_manager
from market_site.config import *

# import random
# import os

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
    last_login = db.Column(db.DateTime, nullable=True, default=datetime.now)
    type = db.Column(db.Integer, default=PHYSICAL_PERSON)
    # company = db.Column(db.String(40), unique=True, nullable=True)      # only if the type==LEGAL_PERSON
    company_id = db.Column(db.Integer, unique=True, nullable=True)      # only if the type==LEGAL_PERSON
    bank_id = db.Column(db.Integer, unique=True, nullable=True)      # only if the type==BANKER

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    balance = db.Column(db.Float, nullable=False, default=0)

    bank_loans = db.relationship('BankLoan', backref='borrower', lazy=True)
    hard_assets = db.relationship('HardAsset', backref='owner', lazy=True)
    company_shares = db.relationship('CompanyShare', backref='owner', lazy=True)
    company_bonds = db.relationship('CompanyBond', backref='owner', lazy=True)
    # auctions = db.relationship("AuctionBidder", backref='bidder', lazy=True)

    total_payments_received = db.Column(db.Float, nullable=True, default=0)
    total_payments_made = db.Column(db.Float, nullable=True, default=0)

    def get_shares(self, company):
        return db.session.query(CompanyShare).filter_by(company_id=company.id, owner_id=self.id).all()

    def share_number(self, company):
        return len(self.get_shares(company))

    def get_bonds(self, company):
        return db.session.query(CompanyBond).filter_by(company_id=company.id, owner_id=self.id).all()

    def bond_number(self, company):
        return len(self.get_bonds(company))

    def share_value(self, company):
        return self.share_number(company) * company.share_value
    
    def share_percentage(self, company):
        n = company.share_number()
        if n > 0:
            return self.share_number(company) / company.share_number()
        return 0
    
    def shares(self):
        q = db.session.query(CompanyShare, Company, func.count(CompanyShare.company_id).label('share_number'))\
            .join(User, CompanyShare.owner_id == User.id)\
            .join(Company, CompanyShare.company_id == Company.id)\
            .where(User.id == self.id)\
            .group_by(Company.name)\
            .order_by(desc('share_number'))
        return q.all()
    
    def bonds(self):
        q = db.session.query(CompanyBond, Company, func.count(CompanyBond.company_id).label('bond_number'))\
            .join(User, CompanyBond.owner_id == User.id)\
            .join(Company, CompanyBond.company_id == Company.id)\
            .where(User.id == self.id)\
            .group_by(Company.name)\
            .order_by(desc('bond_number'))
        return q.all()

    def payments_received(self):
        return Transaction.query.filter_by(payee_id=self.id).all()
    
    def payments_made(self):
        return Transaction.query.filter_by(payer_id=self.id).all()

    def pay(self, amount, payee, info=None):
        if (amount <= self.balance) and (amount > 0) and (self.id != payee.id):
            self.make_payment(amount)
            payee.receive_payment(amount)
            t = Transaction(payer_id=self.id, payee_id=payee.id, amount=amount, info=info)
            db.session.add(t)
            db.session.commit()
            return TRANSACTIO_OK
        else:
            return TRANSACTIO_ERROR
    
    def receive_payment(self, amount):
        self.balance += amount
        self.total_payments_received += amount
        round(self.balance, 2)
        round(self.total_payments_received, 2)
    
    def make_payment(self, amount):
        self.balance -= amount
        self.total_payments_made += amount
        round(self.balance, 2)
        round(self.total_payments_made, 2)
    
    def get_company(self):
        return Company.query.get(self.company_id)

    def get_bank(self):
        return Bank.query.get(self.bank_id)
    
    # def take_bank_loan(self, amount, bank_id, hard_asset_id):
    #     aproved = False
    #     if hard_asset_id

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
    time = db.Column(db.DateTime, nullable=True, default=datetime.now)
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
    auctions = db.relationship('Auction', backref='hard_asset', lazy=True)
    mortgages = db.relationship('BankLoan', backref='hard_asset', lazy=True)

    def is_under_mortgage(self):
        if self.mortgages:
            return self.mortgages[-1].status == REPAID
        return False

    # owner1 = db.relationship("User", foreign_keys=[owner_id])

    def is_on_sale(self):
        if self.sales:
            if self.sales[-1].status == FOR_SALE:
                return True
        return False
    
    def is_on_auction(self):
        if self.auctions:
            if self.auctions[-1].status == FOR_SALE:
                return True
        return False

    def get_images(self):
        image_list = []
        try:
            image_list = json.loads(self.images)
            return image_list
        except:
            return False

    def objectify(self):
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value,
            'info': self.info,
            'images': json.loads(self.images),
            'amount': self.amount,
            'type': self.type,
            'owner_id': self.owner_id,
        }

    def to_json(self):
        return json.dumps(self.objectify())

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

    start = db.Column(db.DateTime, nullable=True, default=datetime.now)
    end = db.Column(db.DateTime, nullable=True)

    def sell(self, buyer):
        if buyer.balance >= self.price and buyer != self.hard_asset.owner:
            buyer.pay(self.price, self.hard_asset.owner, info=f"{self}")
            self.buyer_id = buyer.id
            self.hard_asset.owner_id = buyer.id
            self.status = SOLD
            self.end = datetime.now()
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
    bonds = db.relationship('CompanyBond', backref='company', lazy=True)
    legal_person_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    legal_person = db.relationship("User", foreign_keys=[legal_person_id])
    share_value = db.Column(db.Float, nullable=False, default=0)

    # def holding(self, company):
    #     for i in self.shares:
    #         if i.company_id == company.id:
    #             return True
    #         else:
    #             return 

    # def subsidiary(self, company):
    #     pass
    def get_debt(self):
        debt = 0
        for g in self.bonds:
            debt += g.full_value()
        return debt

    def share_number(self):
        return len(self.shares)
    
    def bond_number(self):
        return len(self.bonds)

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
    sales = db.relationship('CompanyShareSale', backref='share', lazy=True)

    def purchase_price(self):
        if len(self.sales) != 0:
            sale = self.sales[-1]
            if sale.status != SOLD:
                return sale.price
        return 0

    def __repr__(self):
        return f'CompanyShare({self.id}, company={self.company_id}, owner={self.owner_id})'



class CompanyShareSale(db.Model):
    __tablename__ = 'company_share_sales'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False, default=0)
    status = db.Column(db.Integer, nullable=False, default=FOR_SALE)
    share_id = db.Column(db.Integer, db.ForeignKey('company_shares.id'))
    seller_id = db.Column(db.Integer, nullable=True)
    buyer_id = db.Column(db.Integer, nullable=True)

    start = db.Column(db.DateTime, nullable=True, default=datetime.now)
    end = db.Column(db.DateTime, nullable=True)

    def sell(self, buyer):
        if buyer.balance >= self.price and buyer != self.share.owner:
            buyer.pay(self.price, self.share.owner, info=f"{self}")
            self.buyer_id = buyer.id
            self.share.owner_id = buyer.id
            self.status = SOLD
            # self.end = datetime.now()
            # set share value to price
            self.share.company.share_value = self.price
            db.session.commit()
            return OK
        return ERROR
    
    def get_buyer(self):
        return User.query.get(self.buyer_id)

    def get_seller(self):
        return User.query.get(self.seller_id)

    def __repr__(self):
        return f'CompanyShareSale({self.id}, price={self.price})'



class CompanyBond(db.Model):
    __tablename__ = 'company_bonds'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    value = db.Column(db.Float, nullable=False, default=0)
    interest_rate = db.Column(db.Float, nullable=False, default=1)
    sales = db.relationship('CompanyBondSale', backref='bond', lazy=True)

    def full_value(self):
        return self.value * self.interest_rate

    def repay_bond(self):
        cost = self.full_value()
        if self.company.legal_person.balance >= cost:
            self.company.legal_person.pay(cost, self.owner)
            self.status = REPAID
        else:
            self.status = DEFAULT
            self.hard_asset.owner_id = self.bank.legal_person_id
        db.session.commit()

    def __repr__(self):
        return f'CompanyBond({self.id}, company={self.company_id}, owner={self.owner_id})'



class CompanyBondSale(db.Model):
    __tablename__ = 'company_bond_sales'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False, default=0)
    status = db.Column(db.Integer, nullable=False, default=FOR_SALE)
    bond_id = db.Column(db.Integer, db.ForeignKey('company_bonds.id'))
    seller_id = db.Column(db.Integer, nullable=True)
    buyer_id = db.Column(db.Integer, nullable=True)

    start = db.Column(db.DateTime, nullable=True, default=datetime.now)
    end = db.Column(db.DateTime, nullable=True)

    def sell(self, buyer):
        if buyer.balance >= self.price and buyer != self.bond.owner:
            buyer.pay(self.price, self.bond.owner, info=f"{self}")
            self.buyer_id = buyer.id
            self.bond.owner_id = buyer.id
            self.status = SOLD
            self.end = datetime.now()
            db.session.commit()
            return OK
        return ERROR
    
    def get_buyer(self):
        return User.query.get(self.buyer_id)

    def get_seller(self):
        return User.query.get(self.seller_id)

    def __repr__(self):
        return f'CompanyBondSale({self.id}, price={self.price})'



class Bank(db.Model):
    __tablename__ = 'banks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    info = db.Column(db.Text, nullable=True)
    images = db.Column(db.Text, nullable=True)
    loans = db.relationship('BankLoan', backref='bank', lazy=True)
    legal_person_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    legal_person = db.relationship("User", foreign_keys=[legal_person_id])
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    auctions = db.relationship('Auction', backref='bank', lazy=True)
    # transaction_commission = db.Column(db.Float, nullable=False, default=1)
    auction_commission = db.Column(db.Float, nullable=False, default=1)

    def get_images(self):
        image_list = []
        try:
            image_list = json.loads(self.images)
            return image_list
        except:
            return False

    def __repr__(self):
        return f'Bank({self.id}, name={self.name})'



class BankLoan(db.Model):
    __tablename__ = 'bank_loans'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False, default=1)
    borrower_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bank_id = db.Column(db.Integer, db.ForeignKey('banks.id'))
    status = db.Column(db.String(20), nullable=False, default=UNPAID)
    interest_rate = db.Column(db.Float, nullable=False, default=1)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    due_date = db.Column(db.DateTime, nullable=False)
    # loan security ot mortgage
    hard_asset_id = db.Column(db.Integer, db.ForeignKey('hard_assets.id'))

    def full_cost(self):
        return self.amount * self.interest_rate

    def set_mortgage(self, hard_asset):
        if hard_asset.value >= self.full_cost():
            self.hard_asset_id = hard_asset.id
            db.session.commit()
            return OK
        return ERROR

    def repay_loan(self):
        cost = self.full_cost()
        if self.borrower.balance >= cost:
            self.borrower.pay(cost, self.lender)
            self.status = REPAID
        else:
            self.status = DEFAULT
            self.hard_asset.owner_id = self.bank.legal_person_id
        db.session.commit()

    def __repr__(self):
        return f'BankLoan({self.id}, amount={self.amount}, status={self.status})'



class PersonalLoans(db.Model):
    __tablename__ = 'personal_loans'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False, default=1)
    borrower_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    borrower = db.relationship("User", foreign_keys=[borrower_id])
    lender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lender = db.relationship("User", foreign_keys=[lender_id])
    status = db.Column(db.String(20), nullable=False, default=UNPAID)
    interest_rate = db.Column(db.Float, nullable=False, default=1)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    due_date = db.Column(db.DateTime, nullable=True)

    def full_cost(self):
        return self.amount * self.interest_rate

    def repay_loan(self):
        cost = self.full_cost()
        if self.borrower.balance >= cost:
            self.borrower.pay(cost, self.lender)
            self.status = REPAID
        else:
            self.status = DEFAULT
        db.session.commit()

    def __repr__(self):
        return f'PersonalLoan({self.id}, amount={self.amount}, status={self.status})'



class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    code = db.Column(db.String(3), nullable=True)
    images = db.Column(db.Text, nullable=True)
    info = db.Column(db.Text, nullable=True)
    income_tax = db.Column(db.Float, nullable=False, default=0)
    capital_tax = db.Column(db.Float, nullable=False, default=0)
    vat = db.Column(db.Float, nullable=False, default=0)
    customs_tax = db.Column(db.Float, nullable=False, default=0)
    banks = db.relationship('Bank', backref='country', lazy=True)

    def __repr__(self):
        return f'Country(name={self.name}, code={self.code})'



class Auction(db.Model):
    __tablename__ = 'auctions'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False, default=FOR_SALE)

    hard_asset_id = db.Column(db.Integer, db.ForeignKey('hard_assets.id'))
    bank_id = db.Column(db.Integer, db.ForeignKey('banks.id'))
    initial_price = db.Column(db.Float, nullable=False, default=0)
    final_price = db.Column(db.Float, nullable=False, default=1)
    security_deposit = db.Column(db.Float, nullable=False, default=1)
    
    seller_id = db.Column(db.Integer, nullable=True)
    buyer_id = db.Column(db.Integer, nullable=True)
    bidders = db.relationship('AuctionBidder', backref='auction', lazy=True)
    bids = db.relationship('AuctionBid', backref='auction', lazy=True)

    start = db.Column(db.DateTime, nullable=True, default=datetime.now)
    end = db.Column(db.DateTime, nullable=False)

    def add_bidder(self, user):
        if user.id != self.seller_id and not self.is_bidder(user):
            if user.balance >= (self.bank.auction_commission + self.security_deposit):
                user.pay(self.bank.auction_commission, self.bank.legal_person, info='Commission')
                user.pay(self.security_deposit, self.bank.legal_person, info='Security deposit')
                bidder = AuctionBidder(auction_id=self.id, user_id=user.id)
                db.session.add(bidder)
                db.session.commit()
                return OK
        return ERROR
    
    def remove_bidder(self, user):
        bidder = self.get_bidder(user)
        for i in bidder.bids:
            db.session.delete(i)
        self.bank.legal_person.pay(self.security_deposit, user, info='Security deposit return')
        db.session.delete(bidder)
        db.session.commit()

    def last_bid(self):
        if len(self.bids) != 0:
            return self.bids[-1]
        return False

    def place_bid(self, user, amount):
        bidder = self.get_bidder(user)
        if bidder and (amount >= self.initial_price) and (amount >= self.final_price):
            self.final_price = round(amount, 2)
            bid = AuctionBid(amount=amount, bidder_id=bidder.id, auction_id=self.id)
            db.session.add(bid)
            db.session.commit()
            return OK
        return ERROR
    
    def get_bids(self, user):
        q = db.session.query(AuctionBid)\
            .join(AuctionBidder, AuctionBid.bidder_id == AuctionBidder.id)\
            .where(AuctionBid.auction_id == self.id, AuctionBidder.user_id == user.id)
        return q.all()

    # def end(self):
    #     pass

    def is_over(self):
        return datetime.now() > self.end

    def get_bidder(self, user):
        return db.session.query(AuctionBidder)\
            .where(AuctionBidder.auction_id == self.id, AuctionBidder.user_id == user.id)\
            .first()

    def is_bidder(self, user):
        return not not self.get_bidder(user)

    def get_buyer(self):
        return User.query.get(self.buyer_id)

    def get_seller(self):
        return User.query.get(self.seller_id)

    def __repr__(self):
        return f'Auction({self.id}, price={self.initial_price}, seller_id={self.seller_id})'



class AuctionBidder(db.Model):
    __tablename__ = 'auction_bidders'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", foreign_keys=[user_id])
    bids = db.relationship('AuctionBid', backref='bidder', lazy=True)

    def last_bid(self):
        if len(self.bids) >= 1:
            return self.bids[-1]
        return False

    def place_bid(self, amount):
        if amount > self.auction.final_price:
            self.auction.final_price = amount
            bid = AuctionBid(amount=amount, bidder_id=self.id, auction_id=self.auction_id)
            db.session.add(bid)
            db.session.commit()
            return OK
        return ERROR

    def __repr__(self):
        return f'AuctionBidder({self.id}, auction={self.auction_id}, user_id={self.user_id})'



class AuctionBid(db.Model):
    __tablename__ = 'auction_bids'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=True, default=datetime.now)
    amount = db.Column(db.Float, nullable=False, default=1)
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.id'))
    bidder_id = db.Column(db.Integer, db.ForeignKey('auction_bidders.id'))

    def __repr__(self):
        return f'AuctionBid({self.id}, auction={self.auction_id}, amount={self.amount})'



# class Trade(db.Model):
#     __tablename__ = 'trades'
#     id = db.Column(db.Integer, primary_key=True)

#     def __repr__(self):
#         return f'Trade({self.id})'



# class TradeOffer(db.Model):
#     __tablename__ = 'trade_offers'
#     id = db.Column(db.Integer, primary_key=True)

#     def __repr__(self):
#         return f'TradeOffer({self.id})'
