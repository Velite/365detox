from datetime import datetime
from peewee import ForeignKeyField, DateTimeField, DoubleField, BigIntegerField, CharField
from models.base import BaseClass
from models.contragent import LegalEntity
from models.ingredient import Ingredient
from models.shipper import Shipper


class Shipment(BaseClass):
	__tablename__ = "shipments"
	IngredientId = ForeignKeyField(Ingredient, related_name = "Shipments")
	ShipperId = ForeignKeyField(Shipper, related_name = "Shipments")
	InnId = ForeignKeyField(LegalEntity, related_name = "Shipments")
	Date = DateTimeField(null = False, default = datetime.now())
	Name = CharField(null = True)
	Quantity = BigIntegerField(null = False, default = 1)
	Price = DoubleField(null = False, default = 0.0)
