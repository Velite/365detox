from flask import Blueprint, render_template, abort, make_response, jsonify, request, url_for
from flask_login import login_required
from models.contragent import Contragent
from models.delivery import Delivery
from models.product import Product
import strings
from utilities import MessagePacket
from views.main import pages, is_logged, is_admin

deliveries = Blueprint("deliveries", __name__, url_prefix = "/deliveries")


@deliveries.route("/", methods = ["GET"])
@login_required
def index():
	return render_template(pages["deliveries"]["template"], title = pages["deliveries"]["title"],
	                       is_logged = is_logged(), is_admin = is_admin(),
	                       deliveries = MessagePacket.generate(Delivery.getall()))


@deliveries.route("/details", methods = ["POST"])
@login_required
def add():
	if not is_admin():
		abort(401)
	return make_response(jsonify(result = Delivery.add_item(MessagePacket.encode(request.data)) > 0,
	                             redirect = url_for("deliveries.index")), 201)


@deliveries.route("/details/<int:delivery_id>", methods = ["PUT"])
@login_required
def update(delivery_id):
	if not is_admin():
		abort(401)
	if not delivery_id or delivery_id < 1:
		abort(404)
	if Delivery.edit_item(MessagePacket.encode(request.data)) < 1:
		abort(404)
	return make_response(jsonify(result = True, redirect = url_for("deliveries.index")), 200)


@deliveries.route("/<int:delivery_id>", methods = ["DELETE"])
@login_required
def delete(delivery_id):
	if not is_admin():
		abort(401)
	if not delivery_id or delivery_id < 1:
		abort(404)
	if Delivery.delete_item(delivery_id) < 1:
		abort(404)
	return make_response(jsonify(result = True), 200)


# @deliveries.route("/all", methods = ["GET"])
# def listall():
# 	if not is_logged():
# 		abort(401)
# 	return make_response(jsonify(deliveries = Delivery.getall()), 200)


@deliveries.route("/details", methods = ["GET"])
@login_required
def new():
	return render_template("delivery_details.html", title = strings.DELIVERIES_NEW, is_logged = is_logged(),
	                       is_admin = is_admin(), products = MessagePacket.generate(Product.getallshort()),
	                       contragents = MessagePacket.generate(Contragent.getallshort()))


@deliveries.route("/details/<int:delivery_id>", methods = ["GET"])
@login_required
def delivery_edit(delivery_id):
	if delivery_id is None or delivery_id < 1:
		abort(404)
	else:
		return render_template("delivery_details.html", title = "{0}: {1}".format(strings.DELIVERIES_EDIT, delivery_id),
		                       is_logged = is_logged(), is_admin = is_admin(),
		                       delivery = MessagePacket.generate(Delivery.getdetails(delivery_id)),
		                       products = MessagePacket.generate(Product.getallshort()),
		                       contragents = MessagePacket.generate(Contragent.getallshort()))


@deliveries.route("/copy/<int:delivery_id>", methods = ["GET"])
@login_required
def delivery_copy(delivery_id):
	if delivery_id is None or delivery_id < 1:
		abort(404)
	else:
		return render_template("delivery_details.html",
		                       title = "{0}: {1}".format(strings.DELIVERIES_NEW_FROMCOPY, delivery_id),
		                       is_logged = is_logged(), is_admin = is_admin(),
		                       delivery = MessagePacket.generate(Delivery.getdetails(delivery_id)), iscopy = "true",
		                       products = MessagePacket.generate(Product.getallshort()),
		                       contragents = MessagePacket.generate(Contragent.getallshort()))
