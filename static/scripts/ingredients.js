var Supplier = function (id, name, commonname, measurecaption, expirationdays) {
    var self = this;
    self.Id = ko.observable(id);
    self.Name = ko.observable(name);
    self.CommonName = ko.observable(commonname);
    self.MeasureCaption = ko.observable(measurecaption);
    self.ExpirationDays = ko.observable(expirationdays);
};

var IngredientsModel = function (ingredients) {
    var self = this;
    self.ingredients = ko.observableArray();
    var items = ko.utils.arrayMap(msgpack.decode(ingredients), function (item) {
        return new Supplier(item.Id, item.Name, item.CommonName, item.MeasureCaption, item.ExpirationDays);
    });
    ko.utils.arrayPushAll(self.ingredients, items);

    self.DeleteIngredient = function (item) {
        var warning = $("#myWarning");
        warning.find("#warningBody").html("Удалить ингредиент: <strong>" + item.Name() + "</strong>?");
        warning.find("#deleteButton").off();
        warning.find("#deleteButton").click(function () {
            warning.find("#deleteButton").off();
            $.ajax({
                method: "DELETE",
                url: "/ingredients/" + item.Id()
            }).done(function (data) {
                if (data.result === true) {
                    self.ingredients.remove(item);
                }
                warning.modal("hide");
            });
        });

        warning.modal();
    };
};