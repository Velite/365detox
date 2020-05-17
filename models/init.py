from .ingredient import Measure, CommonName, Ingredient
from .shipment import Shipment
from .user import User
from .contragent import Contragent, LegalEntity
from .shipper import Shipper
from .product import Product, ProductPriceHistory
from .delivery import Delivery, DeliveryProduct


def db_init(recreate):
	User.init(recreate)
	Contragent.init(recreate)
	LegalEntity.init(recreate)
	Shipper.init(recreate)
	Product.init(recreate)
	ProductPriceHistory.init(recreate)
	Delivery.init(recreate)
	DeliveryProduct.init(recreate)
	Measure.init(recreate)
	CommonName.init(recreate)
	Ingredient.init(recreate)
	Shipment.init(recreate)
	if recreate:
		User.add_item({'Name': "Andrey", 'Login': "Velite", 'Password': "umbraM93$567", 'Role': "Admin"})
		User.add_item({'Name': "Olya", 'Login': "olya", 'Password': "12345", 'Role': "Admin"})
		User.add_item({'Name': "User 1", 'Login': "user1", 'Password': "123", 'Role': "User"})

		Measure.create(Caption = "кг")
		Measure.create(Caption = "л")
		Measure.create(Caption = "шт")

		CommonName.create(Name = "Не указано")
		CommonName.create(Name = "Яблоки")
		CommonName.create(Name = "Бананы")
		CommonName.create(Name = "Клубника")

		Ingredient.add_item({"Name": "Яблоки гольден", "CommonNameId": 2, "MeasureId": 1, "ExpirationDays": 60})
		Ingredient.add_item({"Name": "Яблоки семиренка", "CommonNameId": 2, "MeasureId": 1, "ExpirationDays": 60})
		Ingredient.add_item({"Name": "Бананы Парагвай", "CommonNameId": 3, "MeasureId": 1, "ExpirationDays": 15})
		Ingredient.add_item({"Name": "Груша Конференц", "CommonNameId": 1, "MeasureId": 1, "ExpirationDays": 5})

		entities = [
			{"Inn": "111111", "Kpp": "222222", "Bik": "333333", "BankName": "Some bank 1", "Correspondent": "444444",
			 "Checking": "555555"},
			{"Inn": "666666", "Kpp": "777777", "Bik": "888888", "BankName": "Some bank 2", "Correspondent": "999999",
			 "Checking": "000000"}]
		contragent = {"Name": "Company 1", "Manager": "Ivanov", "Phone": "+79261112233", "Address": "Moscow",
		              "Other": "Comment 1", "Entities": entities}
		Contragent.add_contragent(contragent)
		Contragent.add_contragent(
			{"Name": "Company 3", "Manager": "Petrov", "Phone": "+79151234567", "Address": "SPb",
			 "Other": "Comment 3"})
		Contragent.add_contragent(
			{"Name": "Company 2", "Manager": "Sidorov", "Phone": "+79039876543", "Address": "Somewhere",
			 "Other": "Comment 2"})
		Contragent.add_supplier(
			{"Name": "Company 4", "Manager": "Lebedev", "Phone": "+71234567890", "Address": "Somewhere 4",
			 "Other": "Comment 4"})

		prices = [{"Price": 10.0, "Date": "28.10.2015"}, {"Price": 12.0, "Date": "31.12.2015"},
		          {"Price": 11.0, "Date": "30.11.2015"}]
		product = {"Name": "Product 1", "Position": 1.0, "Barcode": "111111", "StartSale": "22.10.2015",
		           "Prices": prices}
		Product.add_item(product)

		product = {"Name": "Product 111", "Position": 1.0, "Barcode": "", "StartSale": ""}
		Product.add_item(product)

		prices = [{"Price": 22.0, "Date": "28.10.2015"}, {"Price": 25.0, "Date": "30.11.2015"}]
		product = {"Name": "Product 3", "Position": 1.1, "Barcode": "333333", "StartSale": "01.10.2015",
		           "Prices": prices}
		Product.add_item(product)

		product = {"Name": "Product 2", "Position": 1.2, "Barcode": "222222", "StartSale": "22.10.2015", "Prices": []}
		Product.add_item(product)

		positions = [{"Id": 0, "Quantity": 10, "ProductId": 1}, {"Id": 0, "Quantity": 20, "ProductId": 2}]
		Delivery.add_item({"Date": "28.10.2015", "ContragentId": 2, "Positions": positions})

		positions = [{"Id": 0, "Quantity": 10, "ProductId": 1}, {"Id": 0, "Quantity": 20, "ProductId": 2},
		             {"Id": 0, "Quantity": 30, "ProductId": 3}]
		Delivery.add_item({"Date": "11.11.2015", "ContragentId": 3, "Positions": positions})
		Delivery.add_item({"Date": "25.09.2015", "ContragentId": 3, "Positions": positions})
	else:
		User.edit_item({"Id": 1, "Name": "Andrey", "Login": "Velite", "Password": "umbraM93$567", "Role": "Admin"})
		CommonName.update(Name = "Не указано").where(Ingredient.id == 1)
