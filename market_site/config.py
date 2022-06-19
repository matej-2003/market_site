# TRANSACTIO_STATUS = 0
TRANSACTIO_OK = "TRANSACTIO_OK"
TRANSACTIO_ERROR = "TRANSACTIO_ERROR"

# user type
LEGAL_PERSON = 0
PHYSICAL_PERSON = 1
BANKER = 2
GOVERMENT = 3

# hard asset sales status
FOR_SALE = 0
SOLD = 1

REPAID = "REPAID"
UNPAID = "UNPAID"
DEFAULT = "DEFAULT"

MATURE = "MATURE"
IMMATURE = "IMMATURE"

OK = "OK"
ERROR = "ERROR"

# HARD_ASSET_TYPES
ART = "ART"
HISTORICAL_ARTIFACTS = "HISTORICAL_ARTIFACTS"
RARE_EARTHS = "RARE_EARTHS"
PRECIOUS_METALS = "PRECIOUS_METALS"
REAL_ESTATE = "REAL_ESTATE"
OTHER = "OTHER"
TRANSPORT = "TRANSPORT"

class Config:
	SECRET_KEY = 'matej'
	SECRET_KEY = 'db9d83e5da04c64d757ae22411d72f666101789b7ffc7b41b666ff67a7f61da0edf40c290414db5727990af4a1be0522a96a71e68b61b22aeec82c8849f36680'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False