from peewee import CharField, TextField, BooleanField, ForeignKeyField, prefetch
from models.base import BaseClass


class Contragent(BaseClass):
	__tablename__ = "contragents"
	Name = CharField()
	Manager = CharField(null = True)
	Address = CharField(null = True)
	Phone = CharField(null = True)
	Other = TextField(null = True)
	IsSupplier = BooleanField(null = True, default = False)

	@classmethod
	def add_item(cls, item):
		contragent = Contragent.create(Name = item["Name"], Manager = item["Manager"], Phone = item["Phone"],
		                               Address = item["Address"], Other = item["Other"],
		                               IsSupplier = item.get("IsSupplier")).id
		entities = item.get("Entities")
		if entities:
			for entity in entities:
				LegalEntity.create(ParentId = contragent, Inn = entity.get("Inn"), Kpp = entity.get("Kpp"),
				                   Bik = entity.get("Bik"), BankName = entity.get("BankName"),
				                   Correspondent = entity.get("Correspondent"), Checking = entity.get("Checking"))
		return contragent

	@classmethod
	def add_contragent(cls, item):
		item.update(IsSupplier = False)
		return cls.add_item(item)

	@classmethod
	def add_supplier(cls, item):
		item.update(IsSupplier = True)
		return cls.add_item(item)

	@classmethod
	def edit_item(cls, item):
		affected = Contragent.update(Name = item.get("Name"), Manager = item["Manager"], Phone = item["Phone"],
		                             Address = item["Address"], Other = item["Other"]).where(
			Contragent.id == item.get("Id")).execute()
		entities = item.get("Entities")
		if entities:
			for entity in entities:
				if entity.get("IsDeleted"):
					LegalEntity.delete_item(entity.get("Id"))
				elif entity.get("IsNew"):
					LegalEntity.create(ParentId = item.get("Id"), Inn = entity.get("Inn"), Kpp = entity.get("Kpp"),
					                   Bik = entity.get("Bik"), BankName = entity.get("BankName"),
					                   Correspondent = entity.get("Correspondent"), Checking = entity.get("Checking"))
				else:
					LegalEntity.update(ParentId = item.get("Id"), Inn = entity.get("Inn"), Kpp = entity.get("Kpp"),
					                   Bik = entity.get("Bik"), BankName = entity.get("BankName"),
					                   Correspondent = entity.get("Correspondent"),
					                   Checking = entity.get("Checking")).where(
						LegalEntity.id == entity.get("Id")).execute()
		return affected

	@classmethod
	def get_all_contragents(cls):
		full_info = prefetch(Contragent.select().where(Contragent.IsSupplier == False), LegalEntity.select())
		result = []
		for c in full_info.order_by(+Contragent.Name):
			cont = c.todict()
			cont.update(Entities = [e.todict() for e in c.Entities.order_by(-LegalEntity.Inn)])
			result.append(cont)
		return result

	@classmethod
	def get_all_suppliers(cls):
		full_info = prefetch(Contragent.select().where(Contragent.IsSupplier == True), LegalEntity.select())
		result = []
		for c in full_info.order_by(+Contragent.Name):
			cont = c.todict()
			cont.update(Entities = [e.todict() for e in c.Entities.order_by(-LegalEntity.Inn)])
			result.append(cont)
		return result

	@classmethod
	def getallshort(cls):
		return [c for c in Contragent.select(Contragent.id, Contragent.Name).order_by(+Contragent.Name).dicts()]

	@classmethod
	def getdetails(cls, item_id):
		c = Contragent.get(Contragent.id == item_id)
		contragent = c.todict(
			only = [Contragent.id, Contragent.Name, Contragent.Manager, Contragent.Phone, Contragent.Address,
			        Contragent.Other, Contragent.IsSupplier])
		entities = []
		for entity in c.Entities.order_by(-LegalEntity.Inn):
			e = entity.todict()
			entities.append(e)
		contragent.update(Entities = entities)
		return contragent


class LegalEntity(BaseClass):
	__tablename__ = "legals"
	ParentId = ForeignKeyField(Contragent, null = False, related_name = "Entities")
	Inn = CharField(null = True)
	Kpp = CharField(null = True)
	Bik = CharField(null = True)
	BankName = CharField(null = True)
	Correspondent = CharField(null = True)
	Checking = CharField(null = True)
