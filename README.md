# citalnice

float "{:,.2f}".format()
time .strftime('%d/%m/%Y %H:%M:%S')

# Home

templates/home

# My assets
- asset overview	/home/assets
- hard assets		/home/asset/h
- liquid assets		/home/asset/l
	- shares		/home/asset/l/shares
	- bonds			/home/asset/l/bonds

- auctions			/home/auctions/
- auctions			/home/auctions/finnished
- auctions			/home/auctions/active
# - auctions			/home/auctions/resigned_auctions

# - trades			/home/trades/
- sales				/home/sales/
	- hard asset sales		/home/sales/asset/h

	- liquid asset sales	/home/sales/asset/l
		- summary
	- liquid asset sales	/home/sales/asset/l/stock
	- liquid asset sales	/home/sales/asset/l/bond

- loans
	/home/loans
	/home/loans/bank
	/home/loans/personal

- transactions
	/home/transactions
	/home/transactions/made
	/home/transactions/received


templates/borrow

# Borrow money
- banks
- loans

/borrow
/borrow/banks
/borrow/bank/<int:bank_id>
/borrow/bank/<int:bank_id>/loan

/borrow/personal_loan/offer/make
/borrow/personal_loan/offers


templates/transaction

# Transaction
/transaction/<int:id>
/transactions
/transactions/made
/transactions/received



templates/user

# Users
/users
/user/<int:id>

- asset overview	/user/<int:id>/assets

- hard assets		/user/<int:id>/asset/h
- liquid assets		/user/<int:id>/asset/l
	- shares		/user/<int:id>/asset/l/shares
	- bonds			/user/<int:id>/asset/l/bonds

- auctions			/user/<int:id>/auctions/
   - now			/user/<int:id>/auctions/now
   - history		/user/<int:id>/auctions/history

# - trades			/user/<int:id>/trades/
- sales				/user/<int:id>/sales/
	- hard asset sales		/user/<int:id>/sales/asset/h
	- liquid asset sales	/user/<int:id>/sales/asset/l

- loans
	/user/<int:id>/loans
	/user/<int:id>/loans/bank
	/user/<int:id>/loans/personal

- transactions
	/user/<int:id>/transactions
	/user/<int:id>/transactions/made
	/user/<int:id>/transactions/received





templates/hard_assets

# Assets
/asset/h
/asset/l

## hard asset
/asset/h/<int:hard_asset_id>

/asset/h/<int:hard_asset_id>/sale/create
/asset/h/<int:hard_asset_id>/sales/history
/asset/h/<int:hard_asset_id>/sale/edit
/asset/h/<int:hard_asset_id>/sale/delete

/sale/<int:id>/edit
/sale/<int:id>/delete

/asset/h/<int:hard_asset_id>/auction/create
/asset/h/<int:hard_asset_id>/auctions/history
/asset/h/<int:hard_asset_id>/auction/edit
/asset/h/<int:hard_asset_id>/auction/delete

/auction/<int:id>/edit
/auction/<int:id>/delete

# /asset/h/<int:hard_asset_id>/trade/create
# /asset/h/<int:hard_asset_id>/trades/history
# /asset/h/<int:hard_asset_id>/trade/edit
# /asset/h/<int:hard_asset_id>/trade/delete

# /trade/<int:id>/edit
# /trade/<int:id>/delete



templates/liquid_asset

## liquid asset

/asset/l/company/<int:company_id>
/asset/l/company/<int:company_id>/stock
/asset/l/company/<int:company_id>/bonds
-owners
-info



templates/market

# Market
/market
/market/auctions
/market/auction/<int:auction_id>
/market/auction/<int:auction_id>/join
/market/auction/<int:auction_id>/history


/market/assets/h
/market/assets/h/<string:category>
- sale offers



/market/assets/l

/stock/<int:id>
/bond/<int:id>
- owner
- info

/stock/<int:id>/sell
/bond/<int:id>/sell
- owner
- info

/stock/<int:id>/sale/history
/bond/<int:id>/sale/history
- owner
- info


/stock/<int:company_id>/sell
/bond/<int:company_id>/sell
- sell offer


/stock/<int:company_id>/buy
/bond/<int:company_id>/buy
- buy offer


/stocks
/bonds
- all market info

/stocks/<int:company_id>
/bonds/<int:company_id>
- graph sale offers price
- graph buy offers price


/stocks/<int:company_id>/info
/bonds/<int:company_id>/info
- price charts


# API
/api/user
/api/asset/h/
/api/asset/l/
/api/market/
/api/transaction/
/api/
/api/