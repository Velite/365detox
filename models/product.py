from datetime import datetime
from peewee import CharField, FloatField, DateTimeField, ForeignKeyField, prefetch
from models.base import BaseClass
from dateutil import parser
from utilities import DateTime


class Product(BaseClass):
	__tablename__ = "products"
	Name = CharField()
	Position = FloatField(null = True)
	Barcode = CharField(null = True)
	StartSale = DateTimeField(default = DateTime.local2utc(datetime.now()))
	# Photo = BlobField(null = True)

	@classmethod
	def mass_import(cls, data):
		with cls.get_db().atomic():
			result = Product.insert_many(data).execute()
		return result

	@classmethod
	def add_item(cls, item):
		productid = Product.create(Name = item.get("Name"), Position = item.get("Position"),
		                           Barcode = item.get("Barcode"),
		                           StartSale = datetime.today() if not item.get("StartSale") else parser.parse(
			                           item.get("StartSale"))).id
		prices = item.get("Prices")
		if prices:
			for price in prices:
				date = DateTime.local2utc(price.get("Date"))
				ProductPriceHistory.create(ProductId = productid, Price = price.get("Price"), Date = date)
		return productid

	@classmethod
	def edit_item(cls, item):
		affectedrows = Product.update(Name = item.get("Name"), Position = item.get("Position"),
		                              Barcode = item.get("Barcode"),
		                              StartSale = parser.parse(item.get("StartSale"))).where(
			Product.Id == item.get("Id")).execute()
		for price in item.get("Prices"):
			date = DateTime.local2utc(price.get("Date"))
			if price.get("IsDeleted"):
				ProductPriceHistory.delete_item(price.get("Id"))
			elif price.get("IsNew"):
				ProductPriceHistory.create(ProductId = item.get("Id"), Price = price.get("Price"), Date = date)
			else:
				ProductPriceHistory.update(Price = price.get("Price"), Date = date).where(
					ProductPriceHistory.id == price.get("Id")).execute()

		return affectedrows

	@classmethod
	def getall(cls):
		products_with_prices = prefetch(Product.select(), ProductPriceHistory.select())
		prdcts = []
		for i in products_with_prices.order_by(+Product.Position):
			product = i.todict(only = [Product.id, Product.Name, Product.Barcode, Product.Position])
			product.update(StartSale = DateTime.date2string(DateTime.utc2local(i.StartSale)))
			prcs = []
			for price in i.Prices.order_by(-ProductPriceHistory.Date):
				p = price.todict(only = [ProductPriceHistory.id, ProductPriceHistory.Price])
				p.update(Date = DateTime.date2string(DateTime.utc2local(price.Date)))
				prcs.append(p)
			product.update(Prices = prcs)
			prdcts.append(product)
		return prdcts

	@classmethod
	def getallshort(cls):
		return [p for p in Product.select(Product.id, Product.Name).order_by(+Product.Name).dicts()]

	@classmethod
	def getdetails(cls, item_id):
		with cls.get_db().atomic():
			p = Product.get(Product.id == item_id)
			product = p.todict(only = [Product.id, Product.Position, Product.Name, Product.Barcode])
			product.update(StartSale = DateTime.date2string(DateTime.utc2local(p.StartSale)))
			prcs = []
			for price in p.Prices.order_by(-ProductPriceHistory.Date):
				pr = price.todict(only = [ProductPriceHistory.id, ProductPriceHistory.Price])
				pr.update(Date = DateTime.date2string(DateTime.utc2local(price.Date)))
				prcs.append(pr)
			product.update(Prices = prcs)
			return product


class ProductPriceHistory(BaseClass):
	ProductId = ForeignKeyField(Product, null = False, related_name = "Prices")
	Price = FloatField(null = False, default = 0.0)
	Date = DateTimeField(null = False, default = DateTime.local2utc(datetime.now()))
