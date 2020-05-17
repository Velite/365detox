from flask import Blueprint, render_template, abort, make_response, jsonify, request, url_for
from flask_login import login_required, current_user
from models.ingredient import Ingredient, CommonName, Measure
import strings
from utilities import MessagePacket
from views.main import pages, is_admin, is_logged

ingredients = Blueprint("ingredients", __name__, url_prefix = "/ingredients")


@ingredients.route("/", methods = ["GET"])
@login_required
def index():
	return render_template(pages["ingredients"]["template"], title = pages["ingredients"]["title"],
	                       is_logged = current_user.is_authenticated, is_admin = is_admin(),
	                       ingredients = MessagePacket.generate(Ingredient.getall()))


@ingredients.route("/new", methods = ["GET"])
@login_required
def new():
	return render_template(pages["ingredients"]["details"], title = strings.INGREDIENTS_NEW,
	                       is_logged = current_user.is_authenticated,
	                       is_admin = is_admin(), commons = MessagePacket.generate(CommonName.getall()),
	                       measures = MessagePacket.generate(Measure.getall()))


@ingredients.route("/edit/<int:ingredient_id>", methods = ["GET"])
@login_required
def edit(ingredient_id):
	if not ingredient_id or ingredient_id < 1:
		abort(404)
	else:
		ingredient = Ingredient.getdetails(ingredient_id)
		return render_template(pages["ingredients"]["details"],
		                       title = "{0}: {1}".format(strings.INGREDIENTS_EDIT, ingredient.get("Name")),
		                       is_logged = is_logged(), is_admin = is_admin(),
		                       ingredient = MessagePacket.generate(ingredient),
		                       commons = MessagePacket.generate(CommonName.getall()),
		                       measures = MessagePacket.generate(Measure.getall()))


@ingredients.route("/<int:ingredient_id>", methods = ["DELETE"])
@login_required
def delete(ingredient_id):
	if not is_admin():
		abort(401)
	if not ingredient_id or ingredient_id < 1:
		abort(404)
	if Ingredient.delete_item(ingredient_id) < 1:
		abort(404)
	return make_response(jsonify(result = True), 200)


@ingredients.route("/new", methods = ["POST"])
@login_required
def add():
	if not is_admin():
		abort(401)
	return make_response(jsonify(result = Ingredient.add_item(MessagePacket.encode(request.data)) > 0,
	                             redirect = url_for("ingredients.index")), 201)


@ingredients.route("/edit/<int:ingredient_id>", methods = ["PUT"])
@login_required
def update(ingredient_id):
	if not is_admin():
		abort(401)
	if not ingredient_id or ingredient_id < 1:
		abort(404)
	if Ingredient.edit_item(MessagePacket.encode(request.data)) < 1:
		abort(404)
	return make_response(jsonify(result = True, redirect = url_for("ingredients.index")), 200)
