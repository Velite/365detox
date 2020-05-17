from flask import Blueprint, render_template, request, redirect, url_for
from extensions import login_manager
from flask_login import login_user, current_user, logout_user
from models.user import User
import strings

main = Blueprint("main", __name__)
pages = {"index": {"template": "index.html", "title": strings.INDEX},
         "contragents": {"template": "contragents.html", "title": strings.CONTRAGENTS},
         "suppliers": {"template": "suppliers.html", "title": strings.SUPPLIERS},
         "products": {"template": "products.html", "title": strings.PRODUCTS},
         "deliveries": {"template": "deliveries.html", "title": strings.DELIVERIES},
         "users": {"template": "users.html", "title": strings.USERS},
         "ingredients": {"template": "ingredients.html", "details": "ingredient_details.html",
                         "title": strings.INGREDIENTS},
         "shipments": {"template": "shipments.html", "details": "shipment_details.html", "title": strings.SHIPMENTS},
         "login": {"template": "login.html", "title": strings.LOGIN}}


def is_logged():
	return current_user.is_authenticated


def is_admin():
	return is_logged() and current_user.role == "Admin"


def is_allowed_to_edit():
	return is_admin()


@login_manager.user_loader
def load_user(user_id):
	return User.get(User.id == int(user_id))


@main.route("/", methods = ["GET"])
def index():
	return render_template(pages["index"]["template"], title = pages["index"]["title"], is_logged = is_logged(),
	                       is_admin = is_admin())


@main.route("/login", methods = ["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("main.index"))
	if request.method == "GET":
		return render_template(pages["login"]["template"], title = pages["login"]["title"])
	user, is_authenticated = User.authenticate(request.values.get("login"), request.values.get("password"))
	if user and is_authenticated:
		if login_user(user):
			return redirect(request.args.get("next") or url_for("main.index"))

	return render_template(pages["login"]["template"], title = pages["login"]["title"],
	                       error = strings.ERROR_WRONG_PASSWORD)


@main.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("main.login"))
