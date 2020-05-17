var Supplier = function (id, name, manager, phone, address, other, entities) {
    var self = this;
    self.Id = ko.observable(id);
    self.Name = ko.observable(name);
    self.Manager = ko.observable(manager);
    self.Address = ko.observable(address);
    self.Phone = ko.observable(phone);
    self.Other = ko.observable(other);
    self.Entities = ko.observableArray(entities);
    self.IsPopover = ko.observable(false);
    self.IsNew = ko.pureComputed(function () {
        return self.Id() < 1;
    }, self);
    self.Popover = function () {
        self.IsPopover(!self.IsPopover());
    };
};

var SuppliersModel = function (suppliers) {
    var self = this;
    self.suppliers = ko.observableArray();
    var items = ko.utils.arrayMap(msgpack.decode(suppliers), function (item) {
        return new Supplier(item.Id, item.Name, item.Manager, item.Phone, item.Address, item.Other, item.Entities);
    });
    ko.utils.arrayPushAll(self.suppliers, items);

    self.DeleteSupplier = function (item) {
        var warning = $("#myWarning");
        warning.find("#warningBody").html("Удалить поставщика: <strong>" + item.Name() + "</strong>?");
        warning.find("#deleteButton").off();
        warning.find("#deleteButton").click(function () {
            warning.find("#deleteButton").off();
            $.ajax(
                {
                    method: "DELETE",
                    url: "/suppliers/" + item.Id()
                }).done(function (data) {
                    if (data.result === true) {
                        self.suppliers.remove(item);
                    }
                    warning.modal("hide");
                });
        });

        warning.modal();
    };
};