from peewee import CharField, TextField
from models.base import BaseClass


class Shipper(BaseClass):
	__tablename__ = "shippers"
	Name = CharField()
	Phone = CharField(null = True)
	Comment = TextField(null = True)
