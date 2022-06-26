# from market_site import db, bc
from market_site.config import *
from market_site.models import *
import random
import json

db.drop_all()
db.create_all()
names = ["oliver", "noah", "george", "arthur", "freddie", "leo", "theo", "oscar", "charlie", "harry", "archie", "alfie", "jack"]

for name in names[:4]:
    b = User(
        username=name,
        password=bc.generate_password_hash(name),
        email=f"{name}@locahost",
		full_name=name.capitalize(),
        balance=round(random.randrange(1000, 10000), 2)
        # balance=random.randrange(10, 100)
    )
    print(b)
    db.session.add(b)

db.session.commit()


users = User.query.all()

real_estate = [
    ['Grand Hotel New York', 100, 'asset_0.png', REAL_ESTATE],
    ['New York Cetral Bank', 450, 'asset_1.png', REAL_ESTATE],
    ['Geneva Hotel Contnetal', 250, 'asset_2.png', REAL_ESTATE],
    ['Modern villa outside London', 120, 'asset_3.png', REAL_ESTATE],
    ['Grand yacht', 25, 'asset_4.png', TRANSPORT],
    ['Miami beach house', 80, 'asset_5.png', REAL_ESTATE],
    ['House in New Jersey', 30, 'asset_6.png', REAL_ESTATE],
]

for i, asset in enumerate(real_estate):
    ha = HardAsset(
        name = asset[0],
        value = asset[1],
        images = json.dumps([asset[2]]),
        owner_id = random.choice(users).id,
        info = asset[3],
        type = asset[3]
    )
    print(ha)
    db.session.add(ha)
db.session.commit()

precious_metals = [
    ['Gold', 100, 2, 'gold.png', PRECIOUS_METALS],
    ['Silver', 100, 2, 'silver.png', PRECIOUS_METALS],
    ['Platinum', 100, 2, 'platinum.png', PRECIOUS_METALS],
    ['Palladium', 100, 2, 'palladium.png', PRECIOUS_METALS],
]

for i, asset in enumerate(precious_metals):
    ha = HardAsset(
        name = asset[0],
        value = asset[1],
        amount = asset[2],
        images = json.dumps([asset[3]]),
        owner_id = random.choice(users).id,
        info = asset[4],
        type = asset[4]
    )
    print(ha)
    db.session.add(ha)
db.session.commit()

rare_earths = [
    ['Cobalt', 8, 50, 'cobalt.png', RARE_EARTHS],
    ['Copper', 8, 50, 'copper.png', RARE_EARTHS],
    ['Lithium', 8, 50, 'lithium.png', RARE_EARTHS],
    ['Aluminium', 8, 50, 'aluminium.png', RARE_EARTHS],
]

for i, asset in enumerate(rare_earths):
    ha = HardAsset(
        name = asset[0],
        value = asset[1],
        amount = asset[2],
        images = json.dumps([asset[3]]),
        owner_id = random.choice(users).id,
        info = asset[4],
        type = asset[4]
    )
    print(ha)
    db.session.add(ha)
db.session.commit()

historical_artifacts = [
    ['Greywacke Statue Tribute to Isis', 6000, 'greywacke.png', HISTORICAL_ARTIFACTS],
    ['Harrington Commode', 500, 'harrington.png', HISTORICAL_ARTIFACTS],
    ['Pinner Qing Dynasty Vase', 500, 'pinner.png', HISTORICAL_ARTIFACTS],
    ['Rosetta Stone', 500, 'rosetta.png', HISTORICAL_ARTIFACTS],
    ['Diamond Panther Bracelet', 500, 'panther.png', HISTORICAL_ARTIFACTS],
    ['Napoleon\'s Gold-Encrusted Sword', 500, 'napoleon.png', HISTORICAL_ARTIFACTS],
]

for i, asset in enumerate(historical_artifacts):
    ha = HardAsset(
        name = asset[0],
        value = asset[1],
        images = json.dumps([asset[2]]),
        owner_id = random.choice(users).id,
        info = asset[3],
        type = asset[3]
    )
    print(ha)
    db.session.add(ha)
db.session.commit()


art = [
    ['Mona Lisa', 800, 'mona.png', ART],
    ['Girl with a Pearl Earring', 800, 'girl.png', ART],
    ['The Scream', 800, 'scream.png', ART],
    ['Starry Night', 800, 'night.png', ART],
    ['Guernica', 800, 'guernica.png', ART],
    ['Convergence', 800, 'convergence.png', ART],
    ['Whistler\'s Mother', 800, 'mother.png', ART],
]

for i, asset in enumerate(art):
    ha = HardAsset(
        name = asset[0],
        value = asset[1],
        images = json.dumps([asset[2]]),
        owner_id = random.choice(users).id,
        info = asset[3],
        type = asset[3]
    )
    print(ha)
    db.session.add(ha)
db.session.commit()


assets1 = HardAsset.query.all()

for i in assets1:
    ha = HardAssetSale(
        price = i.value,
        hard_asset_id = i.id,
        seller_id = i.owner.id,
    )
    db.session.add(ha)
db.session.commit()


sales = HardAssetSale.query.all()
for i in sales:
    buyer = random.choice(users)
    if buyer.id != i.seller_id:
        print(i.sell(buyer))

for _ in range(20):
    payer = random.choice(User.query.all())
    payee = random.choice(User.query.all())
    print("Transaction ")
    payer.pay(random.randrange(10, 100), payee)

db.session.commit()

countries = [
    ["SI", "Slovenia"],
    ["US", "United States"],
    ["DE", "Germany"],
    ["GB", "United Kingdom"],
    ["ES", "Spain"],
]

for i, c in enumerate(countries):
    tax = random.uniform(0.5, 20)
    u = Country(
        name = c[1],
        code = c[0],
        income_tax = round(random.random() * tax, 2),
        capital_tax = round(random.random() * tax, 2),
        vat = round(random.random() * tax, 2),
        customs_tax = round(random.random() * tax, 2),
    )
    db.session.add(u)
db.session.commit()


bank_names = [
    ['Nova Ljubljanska banka', 'nlb', 100000, 'nlb.png', 1],
    ['Bank of America', 'america', 100000, 'america.png', 2],
    ['Deutsche Bank', 'deutsche', 100000, 'deutsche.png', 3],
    ['Bank of England', 'england', 100000, 'england.png', 4],
    ['JPMorgan Chase', 'jpmorgan', 100000, 'jpmorgan.png', 2],
    ['Intesa Sanpaolo Bank', 'sanpaolo', 100000, 'sampaolo.png', 5],
]

for i, bank in enumerate(bank_names):
    u = User(
        username = bank[1],
        password = bc.generate_password_hash(bank[1]),
        type = LEGAL_PERSON,
        balance = round(bank[2], 2),
    )
    b = Bank(
        name = bank[0],
        images = json.dumps([ bank[3] ]),
        country_id = bank[4],
        auction_commission = round(random.uniform(1, 20), 2)
    )
    db.session.add(u)
    db.session.add(b)
    db.session.commit()
    u.bank_id = b.id
    b.legal_person_id = u.id
    print(b)
db.session.commit()


company_names = [
    ["Walmart Inc.", "walmart", "company_1.png", 9000, "Wal-Mart Stores, Inc., ali samo Walmart je velika ameriška trgovska veriga, ki jo je ustanovil Sam Walton leta 1962. Sedež podjetja je v Bentonvillu, v ameriški zvezni državi Arkansas. Veriga ima v lasti več kot 11 000 trgovin v 28 državah po svetu."],
    ["Amazon.com Inc.", "amazon", "company_2.png", 6700, "Amazon.com, Inc. je multinacionalno trgovsko podjetje, ki posluje elektronsko, s sedežem v mestu Seattle, Washington, Združene države Amerike."],
    ["Tesla, Inc.", "tesla", "company_3.png", 2800, "Tesla Motors je ameriška družba, ki oblikuje, izdeluje in prodaja električne avtomobile."],
    ["Apple Inc.", "apple", "company_4.png", 5000, "Apple Inc. je ameriško podjetje, ki proizvaja tablične in osebne računalnike z lastnim operacijskim sistemom, pametne telefone, mobilne predvajalnike glasbe in razne spletne storitve."],
    ["facebook inc.", "facebook", "company_5.png", 1500, "facebook inc., je ameriško multinacionalno tehnološko podjetje s sedežem v Menlo Parku v Kaliforniji. Je matična organizacija  Instagrama in WhatsAppa ter drugih podružnic."],
    ["Google Inc.", "google", "company_6.png", 3090, "Google je ameriško podjetje, ustanovljeno leta 1998, njegova najbolj znana izdelka sta istoimenski spletni iskalnik Google in spletni brskalnik Google Chrome."],
    ["Microsoft Inc.", "microsoft", "company_7.png", 8000, "Microsoft Corporation je ameriško računalniško podjetje s sedežem v Redmondu, ki sta ga leta 1975 ustanovila Bill Gates in Paul Allen. Microsoft je največje softversko podjetje na svetu z 128.000 zaposlenimi. Najbolj znani izdelki: MS-DOS Microsoft Windows Microsoft Office Microsoft Word Microsoft"],
]


for i, company in enumerate(company_names):
    share_value = random.randint(10, 500)
    u = User(
        username=company[1],
        password=bc.generate_password_hash(company[1]),
        type = LEGAL_PERSON,
        balance = 0,
    )
    b = Company(
        name = company[0],
        images = json.dumps([ company[2] ]),
        value = company[3],
        info = company[4],
        share_value = share_value,
    )
    db.session.add(u)
    db.session.add(b)
    db.session.commit()
    u.company_id = b.id
    b.legal_person_id = u.id
    print(b)
db.session.commit()

companies = Company.query.all()

for i, company in enumerate(companies):
    bond_price = random.randint(10, 200)
    interest_rate = 1 + random.randint(1, 60) / 100
    for i in range(random.randint(1, 3)):
        users = db.session.query(User)\
            .where(User.type == PHYSICAL_PERSON)\
            .all()
            # .where(User.company_id != company.id)\
        share = CompanyShare(
            owner_id = random.choice(users).id,
            company_id = company.id,
        )
        bond = CompanyBond(
            owner_id = random.choice(users).id,
            company_id = company.id,
            value = bond_price,
            interest_rate = interest_rate,
        )
        db.session.add(share)
        db.session.add(bond)
        print(share)
        print(bond)

db.session.commit()

import time
import datetime

count = 0

for n in range(1):
    print(f"SHARE SALE {n}")
    for c in companies[-3:]:
        for s in c.shares:
            ss = CompanyShareSale(
                price = round(random.uniform(c.share_value, c.share_value * 1.1), 2),
                share_id = s.id,
                seller_id = s.owner_id,
            )
            db.session.add(ss)
            # time.sleep(0.5)
            print(ss)
    # db.session.commit()

    share_sales = db.session.query(CompanyShareSale).where(CompanyShareSale.status == FOR_SALE).all()
    # print(share_sales)

    for ss in share_sales:
        users = db.session.query(User).where(User.type == PHYSICAL_PERSON).filter(User.id != ss.seller_id).all()
        ss.sell(random.choice(users))
        ss.end = datetime.datetime.utcnow() + datetime.timedelta(hours=count)
        # db.session.commit()
        count += 1

db.session.commit()
count = 0

for n in range(1):
    print(f"BOND SALE {n}")
    for c in companies:
        for s in c.bonds[-3:]:
            ss = CompanyBondSale(
                price = round(random.uniform(s.full_value() * 0.3, s.full_value() * 0.8), 2),
                bond_id = s.id,
                seller_id = s.owner_id,
            )
            db.session.add(ss)
            # time.sleep(0.5)
            print(ss)
    # db.session.commit()

    bond_sales = db.session.query(CompanyBondSale).where(CompanyBondSale.status == FOR_SALE).all()
    # print(bond_sales)

    for ss in bond_sales:
        users = db.session.query(User).where(User.type == PHYSICAL_PERSON).filter(User.id != ss.seller_id).all()
        ss.sell(random.choice(users))
        ss.end = datetime.datetime.utcnow() + datetime.timedelta(hours=count)
        # db.session.commit()
        count += 1

db.session.commit()


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
                seller_id = h.owner_id,
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

# GET USERS SHARES
# SELECT users.username, users.id, companies.name as company_name, companies.id, count(company_shares.company_id) as number_of_shares
# FROM company_shares
# INNER JOIN users ON company_shares.owner_id=users.id
# INNER JOIN companies ON company_shares.company_id=companies.id
# where users.id = 4
# group by companies.name
# order by number_of_shares desc;



# r = db.session.query(User.id).\
#             join(User.username).\
#             group_by(User.id)

# SELECT company_shares.id, company_shares.company_id, company_shares.owner_id 
# FROM company_shares
# JOIN users ON company_shares.owner_id = users.id, company_shares
# JOIN companies ON company_shares.company_id = companies.id 
# WHERE users.id = ? GROUP BY company_shares.company_id


# from sqlalchemy import func

# q = db.session.query(func.count(CompanyShare.company_id).label('share_number'), User, Company)\
#     .join(User, CompanyShare.owner_id==User.id)\
#     .join(Company, CompanyShare.company_id==Company.id)\
#     .where(User.id == 4)\
#     .group_by(Company.name)\
#     .order_by('share_number')

# q.all()


# COMPANY SHARES
# SELECT users.username, companies.name, count(companies.name) as share_number
# FROM company_shares
# INNER JOIN users ON company_shares.owner_id=users.id
# INNER JOIN companies ON company_shares.company_id=companies.id
# where users.type = 0
# group by companies.name, users.username
# order by users.username

# select companies.name, count(company_shares.company_id) as share_number
# from companies
# inner join company_shares on company_shares.company_id = companies.id
# group by companies.name;