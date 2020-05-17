from flask import Blueprint, render_template, make_response, json, jsonify, request, abort
from flask_login import fresh_login_required
from models.user import User
import strings
from utilities import MessagePacket
from views.main import pages, is_logged, is_admin

users = Blueprint("users", __name__, url_prefix = "/users")


@users.route("/", methods = ["GET"])
@fresh_login_required
def index():
	if not is_admin():
		abort(405)
	return render_template(pages["users"]["template"], title = pages["users"]["title"], is_logged = is_logged(),
	                       is_admin = is_admin(), users = MessagePacket.generate(User.getall()))


@users.route("/", methods = ["POST"])
@fresh_login_required
def add():
	if not is_admin():
		abort(401)
	newuserid = User.add_item(json.loads(request.values.get("user")))
	if newuserid > 0:
		return make_response(jsonify(result = newuserid), 201)
	elif newuserid == 0:
		return make_response(jsonify(result = strings.ERROR_LOGIN_EXISTS), 500)
	return make_response(jsonify(result = strings.ERROR_EMPTY_PASSWORD), 500)


@users.route("/<int:user_id>", methods = ["PUT"])
@fresh_login_required
def update(user_id):
	if not is_admin():
		abort(401)
	if not user_id or user_id < 1:
		abort(404)
	if User.edit_item(json.loads(request.values.get("user"))) < 1:
		abort(404)
	return make_response(jsonify(result = True), 200)


@users.route("/<int:user_id>", methods = ["DELETE"])
@fresh_login_required
def delete(user_id):
	if not is_admin():
		abort(401)
	if not user_id or user_id < 1:
		abort(404)
	if User.delete_item(user_id) < 1:
		abort(404)
	return make_response(jsonify(result = True), 200)

# @users.route("/all", methods = ["GET"])
# def listall():
# 	if not is_admin():
# 		abort(401)
# 	return make_response(jsonify(users = User.getall()), 200)
