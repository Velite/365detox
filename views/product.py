import os
import tempfile
from flask import Blueprint, render_template, abort, make_response, json, jsonify, request, url_for, session
from flask_login import login_required
from models.product import Product
import strings
from utilities import MessagePacket, Excel
from views.main import pages, is_logged, is_admin

products = Blueprint("products", __name__, url_prefix = "/products")


@products.route("/", methods = ["GET"])
@login_required
def index():
	return render_template(pages["products"]["template"], title = pages["products"]["title"], is_logged = is_logged(),
	                       is_admin = is_admin(), products = MessagePacket.generate(Product.getall()))


@products.route("/details", methods = ["GET"])
@login_required
def new():
	return render_template("product_details.html", title = strings.PRODUCTS_NEW, is_logged = is_logged(),
	                       is_admin = is_admin())


@products.route("/details", methods = ["POST"])
def add():
	if not is_admin():
		abort(401)
	return make_response(jsonify(result = Product.add_item(json.loads(request.values.get("product"))) > 0,
	                             redirect = url_for("products.index")), 201)


@products.route("/details/<int:product_id>", methods = ["PUT"])
def update(product_id):
	if not is_admin():
		abort(401)
	if not product_id or product_id < 1:
		abort(404)
	if Product.edit_item(json.loads(request.values.get("product"))) < 1:
		abort(404)
	return make_response(jsonify(result = True, redirect = url_for("products.index")), 200)


@products.route("/<int:product_id>", methods = ["DELETE"])
def delete(product_id):
	if not is_admin():
		abort(401)
	if not product_id or product_id < 1:
		abort(404)
	if Product.delete_item(product_id) < 1:
		abort(404)
	return make_response(jsonify(result = True), 200)


@products.route("/short")
def listshort():
	if not is_logged():
		abort(401)
	return make_response(jsonify(products = Product.getallshort()), 200)


@products.route("/details/<int:product_id>", methods = ["GET"])
@login_required
def product_edit(product_id):
	if product_id is None or product_id < 1:
		abort(404)
	else:
		product = Product.getdetails(product_id)
		return render_template("product_details.html",
		                       title = "{0}: {1}".format(strings.PRODUCTS_EDIT, product.get("Name")),
		                       is_logged = is_logged(), is_admin = is_admin(), product = json.dumps(product))


@products.route("/import", methods = ["GET", "POST"])
@login_required
def products_import():
	headers = None
	if request.method == "POST" and "importfile" in request.files:
		file = request.files["importfile"]
		if file:
			filename = os.path.join(tempfile.gettempdir(), "{0}_products.xlsx".format(session["user"]))
			file.save(filename)
			session["products_filename"] = filename
			session["products_fileexists"] = True
			headers = Excel.get_headers(file.stream)

	return render_template("products_import.html", title = strings.PRODUCTS_IMPORT, is_logged = is_logged(),
	                       is_admin = is_admin(),
	                       headers = MessagePacket.generate(headers) if headers else "")


@products.route("/finalimport", methods = ["POST"])
@login_required
def products_finalimport():
	fields = MessagePacket.encode(request.data)
	res = False
	if fields and session["products_fileexists"] and session["products_filename"]:
		data = Excel.get_data(session["products_filename"], fields)
		res = Product.mass_import(data)
		if os.path.exists(session["products_filename"]):
			os.remove(session["products_filename"])
			session.pop("products_filename", None)
			session.pop("products_fileexists", False)
	return make_response(jsonify(result = res, redirect = url_for("products.index")), 201)
