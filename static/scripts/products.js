var Product = function (id, position, name, barcode, startsale, prices) {
    var self = this;
    self.Id = ko.observable(id);
    self.Position = ko.observable(position);
    self.Name = ko.observable(name);
    self.Barcode = ko.observable(barcode);
    self.StartSale = ko.observable(startsale);
    self.Prices = ko.observableArray(prices);
    self.IsPopover = ko.observable(false);
    self.Price = ko.observable(0);
    self.IsNew = ko.pureComputed(function () {
        return self.Id() < 1;
    }, self);
    self.Popover = function () {
        self.IsPopover(!self.IsPopover());
    };

    self.ComputePrice = function () {
        var id = 0;
        var days = 2147483647;
        var today = moment();
        ko.utils.arrayForEach(self.Prices(), function (price) {
            price.Active = ko.observable(false);
            var diff = today.diff(moment(price.Date, "DD.MM.YYYY"), "days");
            if (diff >= 0 && diff < days) {
                id = price.id;
                days = diff;
            }
        });
        if (id > 0) {
            var item = ko.utils.arrayFirst(self.Prices(), function (price) {
                return price.id === id;
            });
            self.Price(item.Price);
            item.Active(true);
        }
    };

    self.ComputePrice();
};

var ProductsModel = function (products) {
    var self = this;
    self.products = ko.observableArray();
    if (typeof products !== "undefined" && products != null && products.length > 0) {
        products = msgpack.decode(products);
        var items = ko.utils.arrayMap(products, function (item) {
            return new Product(item.id, item.Position, item.Name, item.Barcode, item.StartSale, item.Prices);
        });
        ko.utils.arrayPushAll(self.products, items);
    }
    self.DeleteProduct = function (item) {
        var warning = $("#myWarning");
        warning.find("#warningBody").html("Удалить номенклатуру: <strong>" + item.Name() + "</strong>?");
        warning.find("#deleteButton").off();
        warning.find("#deleteButton").click(function () {
            warning.find("#deleteButton").off();
            $.ajax(
                {
                    method: "DELETE",
                    url: "/products/" + item.Id()
                }).done(function (data) {
                    if (data.result === true) {
                        self.products.remove(item);
                    }
                    warning.modal("hide");
                });
        });

        warning.modal();
    };
};