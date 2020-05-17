from peewee import PrimaryKeyField
from playhouse.shortcuts import model_to_dict
from extensions import database


class BaseClass(database.Model):
	id = PrimaryKeyField()

	@staticmethod
	def get_db():
		return database.database

	@classmethod
	def init(cls, recreate):
		if recreate:
			cls.drop_table(True)
		if not cls.table_exists():
			cls.create_table(True)

	@classmethod
	def add_item(cls, item):
		pass

	@classmethod
	def edit_item(cls, item):
		pass

	@classmethod
	def delete_item(cls, item_id):
		return cls.get(cls.id == item_id).delete_instance()

	def todict(self, recurse = False, backrefs = False, only = None):
		return model_to_dict(self, recurse = recurse, backrefs = backrefs, only = only)
