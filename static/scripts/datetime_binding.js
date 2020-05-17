ko.bindingHandlers.makeCalendar = {
    init: function (element, accessor) {
        $(element.parentElement).datetimepicker({locale: "ru", format: "DD.MM.YYYY"});
        ko.utils.registerEventHandler(element.parentElement, "dp.change", function (event) {
            var value = accessor();
            if (ko.isObservable(value)) {
                if (event.oldDate != null && event.date != event.oldDate) {
                    value(event.date.format("DD.MM.YYYY"));
                }
            }
        });
    },
    update: function (element, accessor) {
        $(element).val(ko.unwrap(accessor()));
    }
};