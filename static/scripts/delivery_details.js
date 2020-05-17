var Position = function (id, quantity, product) {
    var self = this;
    self.Id = ko.observable(id);
    self.Quantity = ko.observable(quantity);
    self.ProductId = ko.observable(product);
    self.IsDeleted = ko.observable(false);
    self.IsNew = ko.pureComputed(function () {
        return self.Id() < 1;
    }, self);
    self.Remove = function () {
        self.IsDeleted(true);
    };
    self.Export = function () {
        return {
            Id: self.Id(),
            Quantity: parseInt(self.Quantity()),
            ProductId: self.ProductId(),
            IsDeleted: self.IsDeleted(),
            IsNew: self.IsNew()
        };
    };
};

var DeliveryModel = function (delivery, iscopy, products, contragents) {
    var self = this;
    self.Id = ko.observable(0);
    self.Date = ko.observable(moment().format("DD.MM.YYYY"));
    self.ContragentId = ko.observable(0);
    self.Contragents = ko.observableArray(msgpack.decode(contragents));
    self.Products = ko.observableArray(msgpack.decode(products));
    self.Positions = ko.observableArray([]);

    if (typeof delivery !== "undefined" && delivery != null && delivery.length > 0) {
        delivery = msgpack.decode(delivery);
        if (!iscopy) {
            self.Id(delivery.Id);
        }
        self.Date(delivery.Date);
        self.ContragentId(delivery.ContragentId);
        var items = ko.utils.arrayMap(delivery.Products, function (item) {
            return new Position(iscopy ? 0 : item.Id, item.Quantity, item.ProductId);
        });
        ko.utils.arrayPushAll(self.Positions, items);
    }

    self.IsNew = ko.pureComputed(function () {
        return self.Id() < 1;
    }, self);

    self.VisibleRowsCount = ko.pureComputed(function () {
        return ko.utils.arrayFilter(self.Positions(), function (position) {
            return !position.IsDeleted();
        }).length;
    }, self);

    self.Export = function () {
        var positions = ko.utils.arrayMap(self.Positions(), function (item) {
            return !(item.IsNew() && item.IsDeleted());
        });
        var copy = {
            Id: self.Id(),
            Date: self.Date(),
            ContragentId: self.ContragentId(),
            Positions: ko.utils.arrayMap(positions, function (position) {
                return position.Export();
            })
        };
        return msgpack.encode(copy);
    };

    self.Add = function () {
        self.Positions.push(new Position(0, 1, 0));
    };

    self.Save = function () {
        if (!self.IsNew()) {
            $.ajax(
                {
                    method: "PUT",
                    processData: false,
                    contentType: "application/octet-stream",
                    url: "/deliveries/details/" + self.Id(),
                    data: self.Export()
                }).done(function (data) {
                    if (data.result === true) {
                        window.location.replace(data.redirect);
                    }
                });
        }
        else {
            $.ajax(
                {
                    method: "POST",
                    processData: false,
                    contentType: "application/octet-stream",
                    url: "/deliveries/details",
                    data: self.Export()
                }).done(function (data) {
                    if (data.result === true) {
                        window.location.replace(data.redirect);
                    }
                });
        }
    };
};