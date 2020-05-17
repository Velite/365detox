var Price = function (id, price, date) {
    var self = this;
    self.Id = ko.observable(id);
    self.Date = ko.observable(date);
    self.Price = ko.observable(price);
    self.IsNew = ko.pureComputed(function () {
        return self.Id() < 1;
    }, self);
    self.IsDeleted = ko.observable(false);
    self.Remove = function () {
        self.IsDeleted(true);
    };
    self.Active = ko.observable(false);
};

var ProductModel = function (product) {
    var self = this;
    self.Id = ko.observable(0);
    self.Position = ko.observable("");
    self.Name = ko.observable("");
    self.Barcode = ko.observable("");
    self.StartSale = ko.observable("");
    self.Prices = ko.observableArray([]);
    if (typeof product !== "undefined") {
        self.Id(product.Id).Position(product.Position).Name(product.Name).Barcode(product.Barcode).StartSale(product.StartSale);
        var items = ko.utils.arrayMap(product.Prices, function (item) {
            return new Price(item.Id, item.Price, item.Date);
        });
        ko.utils.arrayPushAll(self.Prices, items);
    }

    self.IsNew = ko.pureComputed(function () {
        return self.Id() < 1;
    }, self);

    self.VisibleRowsCount = ko.pureComputed(function () {
        return ko.utils.arrayFilter(self.Prices(), function (price) {
            return !price.IsDeleted();
        }).length;
    }, self);

    self.currentPrice = ko.pureComputed(function () {
        var result = "";
        var id = 0;
        var days = 2147483647;
        var today = moment();
        ko.utils.arrayForEach(self.Prices(), function (price) {
            var diff = today.diff(moment(price.Date(), "DD.MM.YYYY"), "days");
            if (diff >= 0 && diff < days) {
                id = price.Id();
                days = diff;
            }
        });
        if (id > 0) {
            var item = ko.utils.arrayFirst(self.Prices(), function (price) {
                return price.Id() === id;
            });
            result = "Текущая цена: " + item.Price() + " р. от " + item.Date();
            item.Active(true);
        }
        return result;
    }, self);

    self.export = function () {
        var copy = ko.toJS(self);
        delete copy.VisibleRowsCount;
        delete copy.currentPrice;
        return ko.toJSON(copy);
    };

    self.Add = function () {
        self.Prices.push(new Price(0, null, moment().format("DD.MM.YYYY")));
    };

    self.Save = function () {
        ko.utils.arrayForEach(self.Prices(), function (item) {
            if (typeof item !== "undefined" && item.IsNew() && item.IsDeleted()) {
                self.Prices.remove(item);
            }
        });
        if (!self.IsNew()) {
            $.ajax(
                {
                    method: "PUT",
                    url: "/products/details/" + self.Id(),
                    data: {product: self.export()}
                }).done(function (data) {
                    if (data.result === true) {
                        window.location.replace(data.redirect);
                    }
                });
        }
        else {
            $.post("/products/details", {product: self.export()}).done(function (data) {
                if (data.result === true) {
                    window.location.replace(data.redirect);
                }
            });
        }
    };
};