from peewee import TextField, ForeignKeyField, CharField, IntegerField, prefetch
from .base import BaseClass


class CommonName(BaseClass):
	__tablename__ = "commons"
	Name = TextField(null = False)

	@classmethod
	def getall(cls):
		return [cn for cn in CommonName.select(CommonName.id, CommonName.Name).order_by(+CommonName.Name).dicts()]


class Measure(BaseClass):
	__tablename__ = "measures"
	Caption = CharField(null = False)

	@classmethod
	def getall(cls):
		return [m for m in Measure.select(Measure.id, Measure.Caption).order_by(+Measure.Caption).dicts()]


class Ingredient(BaseClass):
	__tablename__ = "ingredients"
	Name = TextField()
	CommonNameId = ForeignKeyField(CommonName, related_name = "Ingredients")
	MeasureId = ForeignKeyField(Measure, related_name = "Ingredients")
	ExpirationDays = IntegerField(null = False, default = 0)

	@classmethod
	def add_item(cls, item):
		commonnameid = item.get("CommonNameId")
		if not commonnameid:
			commonnameid = CommonName.create(Name = item.get("CommonName"))
		ingredient = Ingredient.create(Name = item.get("Name"), CommonNameId = commonnameid,
		                               MeasureId = item.get("MeasureId"),
		                               ExpirationDays = item.get("ExpirationDays")).id
		return ingredient

	@classmethod
	def edit_item(cls, item):
		commonnameid = item.get("CommonNameId")
		if not commonnameid:
			commonnameid = CommonName.create(Name = item.get("CommonName"))
		affected = Ingredient.update(Name = item.get("Name"), CommonNameId = commonnameid,
		                             MeasureId = item.get("MeasureId"),
		                             ExpirationDays = item.get("ExpirationDays")).where(
			Ingredient.id == item.get("Id")).execute()

		return affected

	@classmethod
	def getall(cls):
		alli = prefetch(Ingredient.select(), CommonName.select(), Measure.select())
		return [{"Id": i.id, "Name": i.Name, "ExpirationDays": i.ExpirationDays, "CommonName": i.CommonNameId.Name,
		         "MeasureCaption": i.MeasureId.Caption} for i in alli.order_by(+Ingredient.Name)]

	@classmethod
	def getdetails(cls, item_id):
		i = Ingredient.get(Ingredient.id == item_id)
		ingredient = i.todict()
		return ingredient
