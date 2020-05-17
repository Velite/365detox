from datetime import datetime
from peewee import DateTimeField, ForeignKeyField, BigIntegerField, prefetch
from models.base import BaseClass
from models.contragent import Contragent
from models.product import Product
from utilities import DateTime


class Delivery(BaseClass):
	__tablename__ = "deliveries"
	Date = DateTimeField(null = False, default = datetime.now())
	Contragent = ForeignKeyField(Contragent, null = False, related_name = "Deliveries")

	@classmethod
	def add_item(cls, item):
		delivery = Delivery.create(Date = item.get("Date"), Contragent = item.get("ContragentId")).id
		positions = item.get("Positions")
		if positions:
			for position in positions:
				DeliveryProduct.create(Delivery = delivery, Product = position.get("ProductId"),
				                       Quantity = position.get("Quantity"))
		return delivery

	@classmethod
	def edit_item(cls, item):
		affected = Delivery.update(Date = item.get("Date"), Contragent = item.get("ContragentId")).where(
			Delivery.id == item.get("Id")).execute()
		positions = item.get("Positions")
		if positions:
			for position in positions:
				if position.get("IsDeleted"):
					DeliveryProduct.delete_item(position.get("Id"))
				elif position.get("IsNew"):
					DeliveryProduct.create(Delivery = item.get("Id"), Product = position.get("ProductId"),
					                       Quantity = position.get("Quantity"))
				else:
					DeliveryProduct.update(Delivery = item.get("Id"), Product = position.get("ProductId"),
					                       Quantity = position.get("Quantity")).where(
						DeliveryProduct.id == position.get("Id")).execute()
		return affected

	@classmethod
	def getall(cls):
		d = Delivery.select()
		dp = DeliveryProduct.select()
		c = Contragent.select(Contragent.id, Contragent.Name)
		p = Product.select(Product.id, Product.Name)
		alld = prefetch(d, c, dp, p)

		return sorted([dict(Id = a.id, Date = DateTime.date2string(DateTime.utc2local(a.Date)),
		                    Contragent = a.Contragent.Name, Products = sorted(
				[dict(Name = p.Product.Name, Quantity = p.Quantity) for p in a.Products_prefetch],
				key = lambda x: x["Name"])) for a in alld], key = lambda x: DateTime.parse2date(x["Date"]),
		              reverse = True)

	@classmethod
	def getdetails(cls, item_id):
		delivery = Delivery.get(Delivery.id == item_id)
		res = dict(Id = delivery.id, Date = DateTime.date2string(DateTime.utc2local(delivery.Date)))
		res.update(ContragentId = delivery.Contragent.id)
		products = []
		for p in delivery.Products:
			prd = p.todict(only = [DeliveryProduct.id, DeliveryProduct.Quantity])
			prd.update(ProductId = p.Product.id)
			products.append(prd)
		res.update(Products = products)
		return res


class DeliveryProduct(BaseClass):
	__tablename__ = "product_deliveries"
	Quantity = BigIntegerField(null = False, default = 1)
	Product = ForeignKeyField(Product, null = False, related_name = "Deliveries")
	Delivery = ForeignKeyField(Delivery, null = False, related_name = "Products")
