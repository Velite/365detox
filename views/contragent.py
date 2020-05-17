from flask import Blueprint, render_template, abort, make_response, jsonify, request, url_for
from models.contragent import Contragent
import strings
from utilities import MessagePacket
from views.main import pages, is_logged, is_admin
from flask_login import login_required

contragents = Blueprint("contragents", __name__, url_prefix = "/contragents")


@contragents.route("/", methods = ["GET"])
@login_required
def index():
	return render_template(pages["contragents"]["template"], title = pages["contragents"]["title"],
	                       is_logged = is_logged(), is_admin = is_admin(),
	                       contragents = MessagePacket.generate(Contragent.get_all_contragents()))


@contragents.route("/details", methods = ["GET"])
@login_required
def new():
	return render_template("contragent_details.html", title = strings.NEW_CONTRAGENT, is_logged = is_logged(),
	                       is_admin = is_admin())


@contragents.route("/details", methods = ["POST"])
@login_required
def add():
	if not is_admin():
		abort(401)
	return make_response(jsonify(result = Contragent.add_contragent(MessagePacket.encode(request.data)) > 0,
	                             redirect = url_for("contragents.index")), 201)


@contragents.route("/details/<int:contragent_id>", methods = ["PUT"])
@login_required
def update(contragent_id):
	if not is_admin():
		abort(401)
	if not contragent_id or contragent_id < 1:
		abort(404)
	if Contragent.edit_item(MessagePacket.encode(request.data)) < 1:
		abort(404)
	return make_response(jsonify(result = True, redirect = url_for("contragents.index")), 200)


@contragents.route("/<int:contragent_id>", methods = ["DELETE"])
@login_required
def delete(contragent_id):
	if not is_admin():
		abort(401)
	if not contragent_id or contragent_id < 1:
		abort(404)
	if Contragent.delete_item(contragent_id) < 1:
		abort(404)
	return make_response(jsonify(result = True), 200)


@contragents.route("/short")
@login_required
def listshort():
	if not is_logged():
		abort(401)
	return make_response(jsonify(contragents = Contragent.getallshort()), 200)


@contragents.route("/details/<int:contragent_id>", methods = ["GET"])
@login_required
def contragent_edit(contragent_id):
	if not contragent_id or contragent_id < 1:
		abort(404)
	else:
		contragent = Contragent.getdetails(contragent_id)
		return render_template("contragent_details.html",
		                       title = "{0}: {1}".format(strings.EDIT_CONTRAGENT, contragent.get("Name")),
		                       is_logged = is_logged(), is_admin = is_admin(),
		                       contragent = MessagePacket.generate(contragent))
