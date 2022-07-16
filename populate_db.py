# from flask.current_app import db, bc
from market_site import db, bc, create_app
from market_site.config import *
from market_site.models import *
import random
import json

app, _ = create_app()
app.app_context().push()
db.drop_all()
db.create_all()

names = ["oliver", "noah", "george", "arthur", "freddie", "leo", "theo", "oscar", "charlie", "harry", "archie", "alfie", "jack"]

for name in names:
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

users = User.query.all()

real_estate = [
	['Grand Hotel New York', 100, 'asset_0.png', REAL_ESTATE],
	['New York Cetral Bank', 450, 'asset_1.png', REAL_ESTATE],
	['Geneva Hotel Contnetal', 250, 'asset_2.png', REAL_ESTATE],
	['Modern villa outside London', 120, 'asset_3.png', REAL_ESTATE],
	['Miami beach house', 80, 'asset_5.png', REAL_ESTATE],
	['House in New Jersey', 30, 'asset_6.png', REAL_ESTATE],
]

real_estate2 = [
	['Beach House', 'beach_house.png', REAL_ESTATE],
	['Beach House', 'beach_house1.png', REAL_ESTATE],
	['Beach House', 'beach_house2.png', REAL_ESTATE],
	['Berlin Hotel', 'berlin_hotel.png', REAL_ESTATE],
	['Berlin House', 'berlin_house.png', REAL_ESTATE],
	['Bojnice Castle', 'bojnice_castle.png', REAL_ESTATE],
	['California House', 'california_house.png', REAL_ESTATE],
	['Florida Beach House', 'florida_beach_house.png', REAL_ESTATE],
	['Galveston Mansion', 'galveston_mansion.png', REAL_ESTATE],
	['Germany Mansion', 'germany_mansion.png', REAL_ESTATE],
	['Hotel Slovenia', 'hotel_slovenia.png', REAL_ESTATE],
	['Japan Beach House', 'japan_beach_house.png', REAL_ESTATE],
	['London House', 'london_house.png', REAL_ESTATE],
	['Lutetia Hotel', 'lutetia_hotel.png', REAL_ESTATE],
	['Mansion', 'mansion.png', REAL_ESTATE],
	['Mansion', 'mansion2.png', REAL_ESTATE],
	['Mansion', 'mansion3.png', REAL_ESTATE],
	['Old Mansion', 'old_mansion.png', REAL_ESTATE],
	['Palace Hotel', 'palace_hotel.png', REAL_ESTATE],
	['Paris House', 'paris_house.png', REAL_ESTATE],
	['Pool House', 'pool_house.png', REAL_ESTATE],
	['Scotland House', 'scotland_house.png', REAL_ESTATE],
	['Uk House', 'uk_house.png', REAL_ESTATE],
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

for i, asset in enumerate(real_estate2):
	ha = HardAsset(
		name = asset[0],
		value = random.randint(1, 1000) * 100,
		images = json.dumps([asset[1]]),
		owner_id = random.choice(users).id,
		info = asset[0],
		type = asset[2]
	)
	print(ha)
	db.session.add(ha)

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


historical_artifacts = [
	['Greywacke Statue Tribute to Isis', 6000, 'greywacke.png'],
	['Harrington Commode', 500, 'harrington.png'],
	['Pinner Qing Dynasty Vase', 500, 'pinner.png'],
	['Rosetta Stone', 500, 'rosetta.png'],
	['Diamond Panther Bracelet', 500, 'panther.png'],
	['Napoleon\'s Gold-Encrusted Sword', 500, 'napoleon.png'],
]

for i, asset in enumerate(historical_artifacts):
	ha = HardAsset(
		name = asset[0],
		value = asset[1],
		images = json.dumps([asset[2]]),
		owner_id = random.choice(users).id,
		info = asset[1],
		type = HISTORICAL_ARTIFACTS
	)
	print(ha)
	db.session.add(ha)


historical_artifacts1 = [
	["lindisfarne_gospels.png", "Lindisfarne Gospels", "The Lindisfarne Gospels doesn\u2019t need many words of introduction: it\u2019s one of the finest works in the unique style of Hiberno-Saxon or Insular art, combining Mediterranean, Anglo-Saxon and Celtic elements."],
	["hours_of_jeanne_d_evreux.png", "Hours of Jeanne d'Evreux", "All miniatures are in demi-grisaille, a painting technique using mainly shades of grey and coloring for the figures\u2019 face and hands. The surprising amount of details that can be fit in such small space is outstanding."],
	["godescalc_evangelistary.png", "Godescalc Evangelistary", "Why is this manuscript so important? In the words of Godescalc himself: Golden words are painted on purple pages, The Thunderer\u2019s shining kingdoms of the starry heavens, Revealed in rose-red blood, disclose the joys of heaven, And the eloquence of God glittering with fitting brilliance Promises the splendid rewards of martyrdom to be gained. "],
	["prayerbook_of_claude_de_france.png", "Prayerbook of Claude de France", "In the words of Roger Wieck, curator of manuscripts at the Morgan Library: \u201cAn artistic triumph\u2026\u201d The personalized prayer book of the French queen Claude de France enchants us especially by its delicate paintings in a charmingly small format of 69 x 49 mm, and even more so by the unusual wealth of illustration it contains."],
	["st_albans_psalter.png", "St. Alban's Psalter", "The lavish miniatures and painted initials form such an expressive and lively colored decoration that one can imagine them moving to the rhythm of music: a fantastic picture gallery from the heyday of English book illumination."],
	["westminster_abbey_bestiary.png", "Westminster Abbey Bestiary", "Out of all the Bestiaries, the Westminster is considered to be one of the most beautiful and richly decorated bestiaries in the world, and is full of all kinds of incredible descriptions, legends and myths.Support Medievalists on Patreon "],
	["vienna_genesis.png", "Vienna Genesis", "Wiener-Genesis It is the most ancient purple manuscript surviving today. The fragment of the Genesis (from the Greek Septuagint translation) is compiled in golden and silver ink, on a beautifully purple-dyed calfskin vellum. Each page contains a lavish miniature depicting the text, for a total of 48 well-preserved images."],
	["black_hours.png", "Black Hours", "The Black Hours is a product of unequalled luxury. All 121 vellum folios are stained in black. To make the writing stand out against the dark background, only white lead and opaque paints were used for the miniatures, and gold and silver ink for the script. Only three of these black parchment manuscripts survive to this day."],
	["morgan_crusader_bible.png", "Morgan Crusader Bible", "In this manuscript history is depicted in great detail, without any text and recalls the Creation of the world, the Righteous Wars and the deeds of the most important characters of the Old Testament. The Crusader\u2019s Bible fascinates through its rich and refined gold embellishment which comes to enhance the luminosity of the colors."],
	["grimani_breviary.png", "Grimani Breviary", "The Grimani Breviary A monumental witness to the splendor of Flemish art produced during the Renaissance. Perhaps an outstanding features of this manuscript is the choice of motifs, which alternate between religious and lay themes."]
]

for i, asset in enumerate(historical_artifacts1):
	ha = HardAsset(
		name = asset[1],
		value = random.randint(1, 100) * 100,
		images = json.dumps([asset[0]]),
		owner_id = random.choice(users).id,
		info = asset[2],
		type = HISTORICAL_ARTIFACTS
	)
	print(ha)
	db.session.add(ha)


historical_artifacts2 =[
	["Buddhist Architecture", "Buddhist_architecture.png"],
	["Chinese Jade Culture", "Chinese-Jade-culture.png"],
	["Chinese Neolithic Period Pottery Jar", "Chinese-Neolithic-period-pottery-jar.png"],
	["Cloissone Ancient China", "cloissone-ancient-china.png"],
	["Constitution Of The United States", "Constitution_of_the_United_States.png"],
	["Han Art", "Han-art.png"],
	["Medieval Coins", "medieval_coins.png"],
	["Roman Armor", "roman_armor.png"],
	["Roman Coins", "roman_coins.png"],
	["Roman Coins", "roman_coins1.png"],
	["Roman Coins", "roman_coins2.png"],
	["Roman Coins", "roman_coins3.png"],
	["Jade Dragon", "1-jade-dragon.png"],
	["Jar Showing A Stork With A Fish And A Stone Axe", "2-jar-showing-a-stork-with-a-fish-and-a-stone-axe-.png"],
	["Basin With A Fish Pattern With A Human Face", "3-basin-with-a-fish-pattern-with-a-human-face.png"],
	["Houmuwu Square Cauldron", "4-houmuwu-square-cauldron.png"],
	["Square Vessel With Four Rams", "5-square-vessel-with-four-rams-.png"],
	["Shell Money", "6-shell-money.png"],
	["Li Vessel", "7-li-vessel.png"],
	["Da Yu", "8-da-yu.png"],
	["Jade Burial Suit With Gold Ties", "9-jade-burial-suit-with-gold-ties.png"],
	["Seal Of The King Of Dian", "10-seal-of-the-king-of-dian.png"],
	["Tomb Figurine Of A Storyteller", "11-tomb-figurine-of-a-storyteller-.png"],
	["Womens Jewelry In Shape Of Horse Head With Deer Antlers", "12-womens-jewelry-in-shape-of-horse-head-with-deer-antlers-.png"],
	["Polychrome Glazed Tomb Figurine Of A Troupe Of Musicians On A Camel", "13-polychrome-glazed-tomb-figurine-of-a-troupe-of-musicians-on-a-camel.png"],
	["Stone Dumplings", "14-dumplings.png"],
	["Wooden Statue Of The Guan Yin Bodhisattva", "15-wooden-statue-of-the-guan-yin-bodhisattva.png"],
	["Jinan Lius Fine Needle Shops Advertisement Bronze Plate", "16-jinan-lius-fine-needle-shops-advertisement-bronze-plate.png"],
	["Phoenix Coronet For Empress Xiaoduan", "17-phoenix-coronet-for-empress-xiaoduan.png"],
	["Edict Announcing Emperor Puyis Abdication", "18-edict-announcing-emperor-puyis-abdication.png"],
	["Armour for a boy, probably for Prince Henry Stuart, 1608", "armour_for_prince_henry_stuart.png"],
	["Chinese Qin Sword with gold openwork handle, 770-476 B.C.", "chinese_qin_sword.png"],
	["Scythian golden comb, 5th century B.C.", "scythian_golden_comb.png"],
	["Knife-and-fork set with Mars and Diana, ivory and iron, 1650-1690", "knife-and-fork_set.png"],
	["Burmese bronze 'dragon' cannon, 1790", "burmese_bronze_dragon_cannon.png"],
	["Lewis chessmen - 12th century chess pieces, most of which are carved in walrus ivory", "lewis_chessmen_chess_pieces.png"],
	["Aztec Stone of the Sun - the exact purpose and meaning of the stone is unclear, 14th-16th century", "aztec_stone_of_the_sun.png"],
	["Berlin Gold Hat - 490 grams of gold, overall height 745 mm, average thickness 0.6 mm. Made in the Late Bronze Age, circa 1000 B.C.", "berlin_gold_hat.png"],
	["Helmet Namban Boshi, circa 1600", "helmet_namban_boshi.png"],
	["Cuirass holed by a cannonball at Waterloo", "cuirass_holed_by_a_cannonball_at_waterloo.png"],
	["Parade shield made by Leone Leoni, Italian sculptor in XVIth century", "parade_shield_made_by_leone_leoni.png"],
	["General Patton's Colt .45 Model, 1873", "general_pattons_colt.png"],
	["Caparison ordered by Swedish royal household in 1621", "caparison.png"],
	["Dunstable Swan Jewel from about 1400", "dunstable_swan_jewel.png"],
	["Top of the Lion Armour's helmet, 16th century, France", "top_of_the_lion_armours_helmet.png"],
	["Elephant armour from 17th century India. It's made up of 5,840 plates and weighs an insane 118kg.", "elephant_armour.png"],
	["The Sword of Emperor Maximilian I", "the_sword_of_emperor_maximilian_i.png"],
	["Eighteenth century make-up kit from England that includes a mirror, pencils and a manicure set.", "make-up_kit_from_england.png"],
	["Gold Silver on Bronze Mycenaean “Lion Hunt” burial dagger. Grave Circle A, Mycenae, Greece 16th century B.C.", "lion_hunt_burial_dagger.png"],
	["Lycurgus Cup - Roman, 4th century goblet that changes color when held up to the light.", "lycurgus_cup.png"],
	["Morion for the Guards of the Elector of Saxony", "morion_for_the_guards_of_the_elector_of_saxony.png"],
	["Peacock Clock from Hermitage Museum. It's a large automaton made for Catherine the Great in 1781.", "peacock_clock.png"],
	["Polish Hussar's half-armour, mid-17th century", "polish_hussars_armor.png"],
	["Pyxid Al Mughira from 968 year.", "pyxid_al_mughira.png"],
	["A golden wreath and ring from the burial of an Odrysian Aristocrat at the Golyamata Mogila Tumulus, mid-4th century B.C", "a_golden_wreath_and_ring.png"],
	["Egyptian ring from the tomb of King Tutankhamen", "egyptian_ring_of_king_tutankhamen.png"],
	["Armoured Dresses, Graz Armoury, Austria, late 16th - early 17th century", "armoured_dresses.png"],
	["Joyeuse - Charlemagne's personal sword", "joyeuse_charlemagnes_personal_sword.png"],
]

for i, asset in enumerate(historical_artifacts2):
	ha = HardAsset(
		name = asset[0],
		value = random.randint(1, 800) * 10,
		images = json.dumps([asset[1]]),
		owner_id = random.choice(users).id,
		info = asset[0],
		type = HISTORICAL_ARTIFACTS
	)
	print(ha)
	db.session.add(ha)

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
		type = ART
	)
	print(ha)
	db.session.add(ha)
# db.session.commit()

art1 = [
	["Raffael", "raffael.png"],
	["The Night Watch", "the_night_watch.png"],
	["Jacques Louis David Napoleon Crossing the Alps Kunsthistorisches Museum", "napoleon_crossing_the_alps.png"],
	["Leonardo da Vinci The Last Supper", "the_last_supper.png"],
	["Claude Monet, Impression, soleil levant, 1872", "claude_monet_soleil_levant.png"],
	["Grant Wood American Gothic", "grant_wood_american_gothic.png"],
	["Gu Kaizhi", "gu_kaizhi.png"],
	["Hans Holbein the Younger The Ambassadors", "the_ambassadors.png"],
	["Michelangelo Creation of Adam", "michelangelo_creation_of_adam.png"],
	["The Persistence of Memory", "the_persistence_of_memory.png"],
	["Vincent van Gogh Self portrait with grey felt hat", "vincent_van_gogh_self_portrait.png"],
]

for i, asset in enumerate(art1):
	ha = HardAsset(
		name = asset[0],
		value = random.randint(1, 100) * 100,
		images = json.dumps([asset[1]]),
		owner_id = random.choice(users).id,
		info = asset[0],
		type = ART
	)
	print(ha)
	db.session.add(ha)

transport = [
	['Grand yacht', 'asset_4.png'],
	['Sail Boat', 'sail_boat.png'],
	['Passenger Ship', 'passenger_ship.png'],
	['Fishing Boat', 'fishing_boat.png'],
	['Grand Yacht', 'grand_yacht2.png'],
	["The G.T. 500CR Classic Shelby Mustang", "shelby_mustang.png"],
	["1957 Aquafarbe-Chevrolets Bel Air", "aquafarbe_chevrolets_bel_air.png"],
	["98 Bright Yellow Propellor Aircraft", "yellow_propellor_aircraft.png"],
	["Cessna Denali and Textron \"Single Engine Turboprop\" (SETP)", "cessna_denali.png"],
	["Gulfstream G650", "gulfstream_g650.png"],
	["PEUGEOT e-208", "peugeot_e_208.png"],
	["Volvo XC90 SUV", "volvo_xc90_suv.png"],
	["278 Vintage Toyota", "278_vintage_toyota.png"],
	["2021 Tesla Model S", "2021_tesla_model_s.png"],
	["Mercedes-Benz G 500 (W464), second generation", "mercedes_benz_g_500.png"],
]

for i, asset in enumerate(transport):
	ha = HardAsset(
		name = asset[0],
		value = random.randint(1, 500) * 100,
		images = json.dumps([asset[1]]),
		owner_id = random.choice(users).id,
		info = asset[0],
		type = TRANSPORT
	)
	print(ha)
	db.session.add(ha)

db.session.commit()


for count in range(10):
	ha = HardAsset.query.all()

	for i, e in enumerate(ha):
		seller = e.owner

		buyer = random.choice(users)
		while buyer == seller:
			buyer = random.choice(users)

		has = HardAssetSale(
			price = round(e.value * random.uniform(1.01, 1.30), 2),
			hard_asset_id = e.id,
			seller_id = seller.id,
			buyer_id = buyer.id,
			status = SOLD,
			end = datetime.now(),
		)
		e.owner_id = buyer.id

		db.session.add(has)

		print(count, i)

	db.session.commit()



for _ in range(20):
	payer = random.choice(User.query.all())
	payee = random.choice(User.query.all())
	amount = random.randrange(10, 100)
	print(f"Transaction ${amount}: {payer.username} -> {payee.username}")
	payer.pay(amount, payee)

# db.session.commit()

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

for i, company in enumerate(companies[:3]):
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

# auctions = Auction.query.all()
# for a in auctions:
#     print(a, a.hard_asset.name)
#     for b in a.bidders:
#         b.place_bid(a.final_price + 10)
#         print(a.id, b.user.username, a.bids)


import datetime

for u in users:
	asset = random.choice(u.hard_assets)
	l = BankLoan(
		amount = asset.value,
		borrower_id = u.id,
		bank_id = random.choice(banks).id,
		interest_rate = round(random.uniform(1.01, 1.2), 4),
		due_date = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 10)),
		hard_asset_id = asset.id,
	)
	db.session.add(l)
	db.session.commit()
	l.pay()
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