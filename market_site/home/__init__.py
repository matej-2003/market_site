from flask import Blueprint, render_template
from flask_login import login_required
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb

home = Blueprint("home", __name__, url_prefix="/home", template_folder="templates")


# from .asset_routes import *
# from .auction_routes import *
# from .sale_routes import *
# from .loan_routes import *
# from .transacion_routes import *

default_breadcrumb_root(home, '.')


from market_site.home import asset_routes
from market_site.home import auction_routes
from market_site.home import sale_routes
from market_site.home import loan_routes
from market_site.home import transacion_routes

@home.route('/')
@login_required
@register_breadcrumb(home, '.', 'Home')
def user_home():
	return render_template('home/home.html', title='Home')
