var Product = function (index, name) {
    var self = this;
    self.Index = ko.observable(index);
    self.Name = ko.observable(name);
};

var ProductsImportModel = function (products) {
    var self = this;
    self.products = ko.observableArray();
    if (typeof products !== "undefined" && products != null && products.length > 0) {
        products = msgpack.decode(products);
        var items = ko.utils.arrayMap(products, function (item) {
            return new Product(item.Index, item.Name);
        });
        ko.utils.arrayPushAll(self.products, items);
    }

    self.Import = function () {
        var result = {
            "Name": $("#nameInput").val(),
            "BarCode": $("#barCodeInput").val(),
            "StartSaleDate": $("#dateInput").val(),
            "Position": $("#positionInput").val()
        };
        $.ajax({
            method: "POST",
            processData: false,
            contentType: "application/octet-stream",
            url: "/products/finalimport",
            data: msgpack.encode(result)
        }).done(function (data) {
            if (data.result === true) {
                window.location.replace(data.redirect);
            }
        });
    };
};