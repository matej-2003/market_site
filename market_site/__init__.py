from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from market_site.config import Config
from flask_breadcrumbs import Breadcrumbs
from jinja2 import filters
from flask_socketio import SocketIO

db = SQLAlchemy()
# db.create_all()
bc = Bcrypt()
socket = SocketIO()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	Breadcrumbs(app=app)

	db.init_app(app)
	bc.init_app(app)
	socket.init_app(app)
	login_manager.init_app(app)

	# @app.template_filter()
	# def time(value, format='%d/%m/%Y %H:%M:%S'):
	# 	"""Convert a datetime to a different format."""
	# 	return value.strftime(format)
	
	# @app.template_filter()
	# def price(value):
	# 	if isinstance(value, float):
	# 		return "{:,.2f}".format(value)
	# 	else:
	# 		return value
	
	@app.template_filter()
	def status(value, *classes):
		return filters.do_mark_safe("<span class=\"status {}\">{}</span>".format(" ".join(classes), value))
	
	@app.template_filter()
	def price(value, *classes):
		if isinstance(value, float):
			return filters.do_mark_safe("<span class=\"m {}\">{}</span>".format(" ".join(classes), "{:,.2f}".format(value)))
		else:
			return value

	@app.template_filter()
	def percent(value, *classes):
		if isinstance(value, float):
			return filters.do_mark_safe("<span class=\"p {}\">{}</span>".format(" ".join(classes), "{:,.2f}".format(value)))
		else:
			return value
	
	@app.template_filter()
	def stime(value):
		return value.strftime('%m/%d/%Y %H:%M:%S')

	@app.template_filter()
	def time(value, *classes):
		return filters.do_mark_safe("<span class=\"t {}\">{}</span>".format(" ".join(classes), value.strftime('%m/%d/%Y %H:%M:%S')))

	@app.template_filter()
	def info(value, other_msg='/'):
		return value if value else other_msg


	app.jinja_env.filters['time'] = time
	app.jinja_env.filters['stime'] = stime
	app.jinja_env.filters['price'] = price
	app.jinja_env.filters['percent'] = percent
	app.jinja_env.filters['status'] = status
	app.jinja_env.filters['info'] = info

	from market_site.home import home
	from market_site.api.routes import api
	from market_site.assets.la_routes import liquid_assets
	from market_site.assets.ha_routes import hard_assets
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

	return app, socket