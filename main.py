from flask import Flask, make_response, jsonify
from models.init import db_init
from views.ingredient import ingredients
from views.main import main
from views.contragent import contragents
from views.product import products
from views.delivery import deliveries
from views.supplier import suppliers
from views.user import users
from extensions import login_manager, database, bcrypt


def create_app(config):
	app = Flask(__name__)

	app.config.from_object(config)

	register_extensions(app)
	register_blueprints(app)
	register_errorhandlers(app)

	return app


def register_blueprints(app):
	app.register_blueprint(main)
	app.register_blueprint(contragents)
	app.register_blueprint(suppliers)
	app.register_blueprint(products)
	app.register_blueprint(deliveries)
	app.register_blueprint(ingredients)
	app.register_blueprint(users)

	return None


def register_extensions(app):
	database.init_app(app)
	db_init(app.config.get("DROP_DB"))
	login_manager.init_app(app)
	login_manager.session_protection = "strong"
	login_manager.login_view = "main.login"
	bcrypt.init_app(app)

	return None


def register_errorhandlers(app):
	def get_error(error):
		return "{0}: {1}".format(error.code, error.name)

	@app.errorhandler(401)
	def unauthorized(error):
		return make_response(jsonify(error = get_error(error)), 401)

	@app.errorhandler(404)
	def not_found(error):
		return make_response(jsonify(error = get_error(error)), 404)

	@app.errorhandler(405)
	def not_allowed(error):
		return make_response(jsonify(error = get_error(error)), 405)

	return None
