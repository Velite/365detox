var Contragent = function (id, name, manager, phone, address, other, entities) {
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

var ContragentsModel = function (contragents) {
    var self = this;
    self.contragents = ko.observableArray();
    var items = ko.utils.arrayMap(msgpack.decode(contragents), function (item) {
        return new Contragent(item.Id, item.Name, item.Manager, item.Phone, item.Address, item.Other, item.Entities);
    });
    ko.utils.arrayPushAll(self.contragents, items);

    self.DeleteContragent = function (item) {
        var warning = $("#myWarning");
        warning.find("#warningBody").html("Удалить контрагента: <strong>" + item.Name() + "</strong>?");
        warning.find("#deleteButton").off();
        warning.find("#deleteButton").click(function () {
            warning.find("#deleteButton").off();
            $.ajax(
                {
                    method: "DELETE",
                    url: "/contragents/" + item.Id()
                }).done(function (data) {
                    if (data.result === true) {
                        self.contragents.remove(item);
                    }
                    warning.modal("hide");
                });
        });

        warning.modal();
    };
};