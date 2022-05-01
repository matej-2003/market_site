from market_site import db, bc, PHYSICAL_PERSON
from market_site import ART, HISTORICAL_ARTIFACTS, RARE_EARTHS, PRECIOUS_METALS, REAL_ESTATE, OTHER, TRANSPORT
from market_site.models import *
import random
import json

db.drop_all()
db.create_all()
names = ["oliver", "noah", "george", "arthur", "freddie", "leo", "theo", "oscar", "charlie", "harry", "archie", "alfie", "jack"]

for name in names[:2]:
    c = User(
        username=name,
        password=bc.generate_password_hash(name),
        email=f"{name}@locahost",
		full_name=name.capitalize(),
        balance=random.randrange(1000, 10000)
        # balance=random.randrange(10, 100)
    )
    print(c)
    db.session.add(c)

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
    print(ha)


# sales = HardAssetSale.query.all()
# for i in sales:
#     buyer = random.choice(users)
#     if buyer.id != i.seller_id:
#         print(i.sell(buyer))

# for _ in range(20):
#     payer = random.choice(User.query.all())
#     payee = random.choice(User.query.all())
#     payer.pay(random.randrange(10, 100), payee)

# db.session.commit()


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
    u = User(
        username=company[1],
        password=bc.generate_password_hash(company[1]),
        type = LEGAL_PERSON,
        balance = 0,
    )
    c = Company(
        name = company[0],
        images = json.dumps([ company[2] ]),
        value = company[3],
        info = company[4],
    )
    db.session.add(u)
    db.session.add(c)
    db.session.commit()
    u.company_id = c.id
    c.legal_person_id = u.id
    print(c)
db.session.commit()

companies = Company.query.all()

for i, company in enumerate(companies):
    for i in range(random.randint(3, 8)):
        users = db.session.query(User)\
            .where(User.type == PHYSICAL_PERSON)\
            .all()
            # .where(User.company_id != company.id)\
        share = CompanyShare(
            owner_id = random.choice(users).id,
            company_id = company.id,
        )
        print(share)
        db.session.add(share)
db.session.commit()


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