from flask import Blueprint

home = Blueprint("home", __name__, url_prefix="/home", template_folder="templates")

from market_site.home.asset_routes import *
from market_site.home.auction_routes import *
from market_site.home.sale_routes import *
from market_site.home.loan_routes import *
from market_site.home.transacion_routes import *