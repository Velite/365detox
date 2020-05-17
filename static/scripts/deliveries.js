var Delivery = function (id, date, contragent, products) {
    var self = this;
    self.Id = ko.observable(id);
    self.Date = ko.observable(date);
    self.Contragent = ko.observable(contragent);
    self.Products = ko.observableArray(products);
    self.IsPopover = ko.observable(false);
    self.IsNew = ko.pureComputed(function () {
        return self.Id() < 1;
    }, self);

    self.Popover = function () {
        self.IsPopover(!self.IsPopover());
    }
};

var DeliveriesModel = function (deliveries) {
    var self = this;
    self.deliveries = ko.observableArray([]);

    var items = ko.utils.arrayMap(msgpack.decode(deliveries), function (item) {
        return new Delivery(item.Id, item.Date, item.Contragent, item.Products);
    });
    ko.utils.arrayPushAll(self.deliveries, items);

    self.DeleteDelivery = function (item) {
        var warning = $("#myWarning");
        warning.find("#warningBody").html("Удалить отгрузку: <strong>" + item.Id() + "</strong>?");
        warning.find("#deleteButton").off();
        warning.find("#deleteButton").click(function () {
            warning.find("#deleteButton").off();
            $.ajax(
                {
                    method: "DELETE",
                    url: "/deliveries/" + item.Id()
                }).done(function (data) {
                    if (data.result === true) {
                        self.deliveries.remove(item);
                    }
                    warning.modal("hide");
                });
        });

        warning.modal();
    };
};