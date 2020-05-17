from flask import Blueprint, render_template, abort, make_response, jsonify, request, url_for
from flask_login import login_required
from models.contragent import Contragent
import strings
from utilities import MessagePacket
from views.main import pages, is_logged, is_admin

suppliers = Blueprint("suppliers", __name__, url_prefix = "/suppliers")


@suppliers.route("/", methods = ["GET"])
@login_required
def index():
	return render_template(pages["suppliers"]["template"], title = pages["suppliers"]["title"], is_logged = is_logged(),
	                       is_admin = is_admin(),
	                       suppliers = MessagePacket.generate(Contragent.get_all_suppliers()))


@suppliers.route("/new", methods = ["GET"])
@login_required
def new():
	return render_template("supplier_details.html", title = strings.SUPPLIERS_NEW, is_logged = is_logged(),
	                       is_admin = is_admin())


@suppliers.route("/new", methods = ["POST"])
def add():
	if not is_admin():
		abort(401)
	return make_response(jsonify(result = Contragent.add_supplier(MessagePacket.encode(request.data)) > 0,
	                             redirect = url_for("suppliers.index")), 201)


@suppliers.route("/edit/<int:supplier_id>", methods = ["PUT"])
def update(supplier_id):
	if not is_admin():
		abort(401)
	if not supplier_id or supplier_id < 1:
		abort(404)
	if Contragent.edit_item(MessagePacket.encode(request.data)) < 1:
		abort(404)
	return make_response(jsonify(result = True, redirect = url_for("suppliers.index")), 200)


@suppliers.route("/<int:supplier_id>", methods = ["DELETE"])
def delete(supplier_id):
	if not is_admin():
		abort(401)
	if not supplier_id or supplier_id < 1:
		abort(404)
	if Contragent.delete_item(supplier_id) < 1:
		abort(404)
	return make_response(jsonify(result = True), 200)


# @suppliers.route("/short")
# def listshort():
# 	if not is_logged():
# 		abort(401)
# 	return make_response(jsonify(contragents = Contragent.getallshort()), 200)


@suppliers.route("/edit/<int:supplier_id>", methods = ["GET"])
@login_required
def supplier_edit(supplier_id):
	if not supplier_id or supplier_id < 1:
		abort(404)
	else:
		supplier = Contragent.getdetails(supplier_id)
		return render_template("supplier_details.html",
		                       title = "{0}: {1}".format(strings.SUPPLIERS_EDIT, supplier.get("Name")),
		                       is_logged = is_logged(), is_admin = is_admin(),
		                       supplier = MessagePacket.generate(supplier))
