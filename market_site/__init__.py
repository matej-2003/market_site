from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from market_site.config import Config

db = SQLAlchemy()
# db.create_all()
bc = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	
	db.init_app(app)
	bc.init_app(app)
	login_manager.init_app(app)

	from market_site.api.routes import api
	from market_site.assets.la_routes import liquid_assets
	from market_site.assets.ha_routes import hard_assets
	from market_site.home.routes import home
	from market_site.market.routes import market
	from market_site.auction.routes import auction
	from market_site.users.routes import users

	app.register_blueprint(api)
	app.register_blueprint(liquid_assets)
	app.register_blueprint(hard_assets)
	app.register_blueprint(home)
	app.register_blueprint(market)
	app.register_blueprint(auction)
	app.register_blueprint(users)

	return app