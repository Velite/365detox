from datetime import datetime
from flask_login import UserMixin
from peewee import CharField, DateTimeField, IntegrityError
from extensions import bcrypt
from models.base import BaseClass
from utilities import DateTime


class User(BaseClass, UserMixin):
	__tablename__ = "users"
	name = CharField(null = False)
	login = CharField(null = False, unique = True)
	password = CharField(null = False)
	role = CharField(null = True, default = "Guest")
	lastlogindate = DateTimeField(null = True, default = None)

	@classmethod
	def add_item(cls, item):
		try:
			with cls.get_db().atomic():
				return User.create(name = item.get("Name"), login = item.get("Login"),
				                   password = bcrypt.generate_password_hash(item.get("Password")),
				                   role = item.get("Role")).id
		except IntegrityError:
			return 0
		except ValueError:
			return -1

	@classmethod
	def edit_item(cls, item):
		return User.update(name = item.get("Name"), role = item.get("Role")).where(User.id == item.get("Id")).execute()

	@classmethod
	def getuserbylogin(cls, login):
		if login != "":
			with cls.get_db().atomic():
				return User.get(User.login == login)
		return None

	@classmethod
	def getuserbyid(cls, user_id):
		if user_id > 0:
			with cls.get_db().atomic():
				return User.get(User.id == user_id).first()
		return None

	@classmethod
	def authenticate(cls, login, password):
		if login is not "" and password is not "":
			user = cls.getuserbylogin(login)
			if user is not None:
				if bcrypt.check_password_hash(user.password, password):
					User.update(lastlogindate = DateTime.local2utc(datetime.now())).where(User.id == user.id).execute()
					return user, True
		return None, False

	@classmethod
	def getall(cls):
		tmp = [u for u in
		       User.select(User.id, User.name, User.login, User.role, User.lastlogindate).order_by(User.name).dicts()]

		return [dict(Id = i.id,
		             Login = i.login,
		             Name = i.name,
		             Role = i.role,
		             LastLoginDate = DateTime.datetime2string(
			             DateTime.utc2local(i.lastlogindate)) if i.lastlogindate else None) for i in
		        User.select(User.id, User.name, User.login, User.role, User.lastlogindate).order_by(User.name)]
