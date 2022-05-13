# citalnice

# Home

routes.py
templates/home

# my assets
- asset overview	/home/assets

-hard assets		/home/asset/h
-liquid assets		/home/asset/l
	-shares			/home/asset/l/shares
	-bonds			/home/asset/l/bonds

-auctions			/home/auctions/
-trades				/home/trades/
-sales				/home/sales/
	-hard asset sales		/home/sales/asset/h
	-liquid asset sales		/home/sales/asset/l

-loans
	/home/loans
	/home/loans/bank
	/home/loans/personal

-transactions
	/home/transactions
	/home/transactions/made
	/home/transactions/received


routes.py
templates/borrow

# Borrow money
-banks
-loans

/borrow
/borrow/banks
/borrow/bank/<int:bank_id>
/borrow/bank/<int:bank_id>/loan

/borrow/personal_loan/offer/make
/borrow/personal_loan/offers


routes.py
templates/transaction

# Transaction
/transaction/<int:id>
/transactions
/transactions/made
/transactions/received



routes_user.py
templates/user

# Users
/users
/user/<int:id>

- asset overview	/home/assets

-hard assets	/user/<int:id>/asset/h
-liquid assets	/user/<int:id>/asset/l
	-shares		/user/<int:id>/asset/l/shares
	-bonds		/user/<int:id>/asset/l/bonds

-auctions		/user/<int:id>/auctions/
   -now			/user/<int:id>/auctions/now
   -history		/user/<int:id>/auctions/history

-trades			/user/<int:id>/trades/
-sales			/user/<int:id>/sales/
	-hard asset sales		/user/<int:id>/sales/asset/h
	-liquid asset sales		/user/<int:id>/sales/asset/l

-loans
	/user/<int:id>/loans
	/user/<int:id>/loans/bank
	/user/<int:id>/loans/personal

-transactions
	/user/<int:id>/transactions
	/user/<int:id>/transactions/made
	/user/<int:id>/transactions/received





routes_hard_asset.py
templates/hard_assets

# Assets
/asset/h
/asset/l

## hard asset
/asset/h/<int:hard_asset_id>

/asset/h/<int:hard_asset_id>/sale
/asset/h/<int:hard_asset_id>/sale/edit
/asset/h/<int:hard_asset_id>/sale/delete
/asset/h/<int:hard_asset_id>/sales/history

/asset/h/<int:hard_asset_id>/auction
/asset/h/<int:hard_asset_id>/auction/edit
/asset/h/<int:hard_asset_id>/auction/delete
/asset/h/<int:hard_asset_id>/auctions/history

/asset/h/<int:hard_asset_id>/trade
/asset/h/<int:hard_asset_id>/trade/edit
/asset/h/<int:hard_asset_id>/trade/delete
/asset/h/<int:hard_asset_id>/trades/history




routes_liquid_asset.py
templates/liquid_asset

## liquid asset

/asset/l/company/<int:company_id>
/asset/l/company/<int:company_id>/stock
/asset/l/company/<int:company_id>/bonds
-owners
-info


/asset/l/company/<int:company_id>/stock/sell
/asset/l/company/<int:company_id>/bonds/sell
-sell offer


/bond/<int:id>
/share/<int:id>
-owners
-info

/bond/<int:id>/sale/history
/share/<int:id>/sale/history
-owners
-info






routes_market.py
templates/market

# Market
/market
/market/auctions
/market/auction/<int:auction_id>
/market/auction/<int:auction_id>/join
/market/auction/<int:auction_id>/history


/market/asset/h
/market/asset/h/<string:category>
-sale offers

/market/asset/l

/market/asset/l/bonds
/market/asset/l/stocks
-market info

/market/asset/l/stocks/<int:company_id>
/market/asset/l/bonds/<int:company_id>
-sale offers
-buy offers


/market/asset/l/stocks/<int:company_id>/info
/market/asset/l/bonds/<int:company_id>/info
-charts


routes_api.py

# API
/api/user
/api/asset/h/
/api/asset/l/
/api/market/
/api/transaction/
/api/
/api/