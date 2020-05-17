var IngredientModel = function (ingredient, commons, measures) {
    var self = this;
    self.Id = ko.observable(0);
    self.Name = ko.observable("");
    self.CommonNameId = ko.observable(0);
    self.ExpirationDays = ko.observable(0);
    self.MeasureId = ko.observable(0);
    self.CommonNames = ko.observableArray(msgpack.decode(commons));
    self.CommonName = ko.observable("");
    $("#inputCommonName").typeahead({
        source: self.CommonNames(), displayText: function (item) {
            return item.Name;
        }
    });
    self.Measures = ko.observableArray(msgpack.decode(measures));
    if (typeof ingredient !== "undefined" && ingredient != null && ingredient.length > 0) {
        ingredient = msgpack.decode(ingredient);
        self.Id(ingredient.Id);
        self.Name(ingredient.Name);
        self.CommonNameId(ingredient.CommonNameId);
        self.ExpirationDays(ingredient.ExpirationDays);
        self.MeasureId(ingredient.MeasureId);

        var commonNameMatch = ko.utils.arrayFirst(self.CommonNames(), function (item) {
            return item.Id === self.CommonNameId()
        });
        if (commonNameMatch != null) {
            self.CommonName(commonNameMatch.Name);
        }
    }

    self.IsNew = ko.pureComputed(function () {
        return self.Id() < 1;
    }, self);

    self.Export = function () {
        var commonNameId = ko.utils.arrayFirst(self.CommonNames(), function (item) {
            return item.Name === self.CommonName();
        });
        var copy = {
            Id: parseInt(self.Id()),
            Name: self.Name(),
            ExpirationDays: parseInt(self.ExpirationDays()),
            CommonNameId: commonNameId != null ? parseInt(commonNameId.Id) : 0,
            MeasureId: parseInt(self.MeasureId())
        };
        if (copy.CommonNameId < 1) {
            copy.CommonName = self.CommonName();
        }

        return msgpack.encode(copy);
    };

    self.Save = function () {
        if (!self.IsNew()) {
            $.ajax({
                method: "PUT",
                processData: false,
                contentType: "application/octet-stream",
                url: "/ingredients/edit/" + self.Id(),
                data: self.Export()
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
                url: "/ingredients/new",
                data: self.Export()
            }).done(function (data) {
                if (data.result === true) {
                    window.location.replace(data.redirect);
                }
            });
        }
    };
};