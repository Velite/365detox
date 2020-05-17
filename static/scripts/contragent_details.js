var Entity = function (id, inn, kpp, bik, corr, check, bank) {
    var self = this;
    self.Id = ko.observable(id);
    self.Inn = ko.observable(inn);
    self.Kpp = ko.observable(kpp);
    self.Bik = ko.observable(bik);
    self.Correspondent = ko.observable(corr);
    self.Checking = ko.observable(check);
    self.Bank = ko.observable(bank);
    self.IsNew = ko.pureComputed(function () {
        return self.Id() < 1;
    }, self);
    //self.IsModified = ko.observable(false);
    self.IsDeleted = ko.observable(false);
    self.Remove = function () {
        self.IsDeleted(true);
    };
    self.Export = function () {
        return {
            Id: self.Id(),
            Inn: self.Inn(),
            Kpp: self.Kpp(),
            Bik: self.Bik(),
            Correspondent: self.Correspondent(),
            Checking: self.Checking(),
            BankName: self.Bank(),
            IsDeleted: self.IsDeleted(),
            IsNew: self.IsNew()
        };
    };
};

var ContragentModel = function (contragent) {
    var self = this;
    self.Id = ko.observable(0);
    self.Name = ko.observable("");
    self.Manager = ko.observable("");
    self.Phone = ko.observable("");
    self.Address = ko.observable("");
    self.Other = ko.observable("");
    self.Entities = ko.observableArray([]);
    if (typeof contragent !== "undefined" && contragent != null && contragent.length > 0) {
        contragent = msgpack.decode(contragent);
        self.Id(contragent.Id);
        self.Name(contragent.Name);
        self.Manager(contragent.Manager);
        self.Phone(contragent.Phone);
        self.Address(contragent.Address);
        self.Other(contragent.Other);
        var items = ko.utils.arrayMap(contragent.Entities, function (item) {
            return new Entity(item.Id, item.Inn, item.Kpp, item.Bik, item.Correspondent, item.Checking, item.BankName);
        });
        ko.utils.arrayPushAll(self.Entities, items);
    }

    self.IsNew = ko.pureComputed(function () {
        return self.Id() < 1;
    }, self);

    self.VisibleRowsCount = ko.pureComputed(function () {
        return ko.utils.arrayFilter(self.Entities(), function (entity) {
            return !entity.IsDeleted();
        }).length;
    }, self);

    self.export = function () {
        var entities = ko.utils.arrayFilter(self.Entities(), function (item) {
            return !(item.IsNew() && item.IsDeleted());
        });
        var copy = {
            Id: self.Id(),
            Name: self.Name(),
            Manager: self.Manager(),
            Phone: self.Phone(),
            Address: self.Address(),
            Other: self.Other(),
            Entities: ko.utils.arrayMap(entities, function (entity) {
                return entity.Export();
            })
        };
        return msgpack.encode(copy);
    };

    self.Add = function () {
        self.Entities.push(new Entity(0, null, null, null, null, null, null));
    };

    self.Save = function () {
        if (!self.IsNew()) {
            $.ajax(
                {
                    method: "PUT",
                    processData: false,
                    contentType: "application/octet-stream",
                    url: "/contragents/details/" + self.Id(),
                    data: self.export()
                }).done(function (data) {
                    if (data.result === true) {
                        window.location.replace(data.redirect);
                    }
                });
        }
        else {
            $.ajax({
                method: "POST",
                processData: false,
                contentType: "application/octet-stream",
                url: "/contragents/details",
                data: self.export()
            }).done(function (data) {
                if (data.result === true) {
                    window.location.replace(data.redirect);
                }
            });
        }
    };
};