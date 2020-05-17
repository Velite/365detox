var User = function (id, name, login, password, role, lastlogin) {
    var self = this;
    self.Id = ko.observable(id);
    self.Name = ko.observable(name);
    self.Login = ko.observable(login);
    self.Password = ko.observable(password);
    self.Role = ko.observable(role);
    self.LastLogin = ko.observable(lastlogin);
    self.IsNew = ko.pureComputed(function () {
        return self.Id() < 1;
    }, self);
};

var UsersModel = function (users) {
    var self = this;
    self.users = ko.observableArray();
    var items = ko.utils.arrayMap(msgpack.decode(users), function (item) {
        return new User(item.Id, item.Name, item.Login, "", item.Role, item.LastLoginDate);
    });
    ko.utils.arrayPushAll(self.users, items);

    self.AddUser = function () {
        self.ShowModal(null);
    };

    self.EditUser = function (user) {
        self.ShowModal(user);
    };

    self.SaveUser = function (user) {
        var modal = $("#myModal");
        user.Name(modal.find("#inputName").val());
        user.Login(modal.find("#inputLogin").val());
        user.Password(modal.find("#inputPassword").val());
        user.Role(modal.find("#inputRole").val());
        modal.find("#saveButton").off();

        if (!user.IsNew()) {
            $.ajax(
                {
                    method: "PUT",
                    url: "/users/" + user.Id(),
                    data: {user: ko.toJSON(user)}
                }).done(function () {
                    modal.modal('hide');
                });
        }
        else {
            $.post("/users/", {user: ko.toJSON(user)}).done(function (data) {
                user.Id(data.result);
                self.users.push(user);

                modal.modal('hide');
            }).fail(function (data) {
                var error = modal.find("#errorBlock");
                error.text(data.responseJSON.result);
                error.show();
            });
        }
    };

    self.ShowModal = function (item) {
        if (typeof item === "undefined" || item == null) {
            item = new User(0, "", "", "", "Guest", null);
        }

        var modal = $("#myModal");
        modal.find("#errorBlock").hide();
        modal.find("#modalTitle").text(!item.IsNew() ? "Изменение пользователя" : "Новый пользователь");
        modal.find("#inputName").val(item.Name());
        modal.find("#inputLogin").val(item.Login());
        modal.find("#inputRole").val(item.Role());
        if (!item.IsNew()) {
            modal.find("#inputLogin").attr("disabled", "disabled");
            modal.find("#inputPassword").attr("disabled", "disabled");
            modal.find("#inputPassword").val("password");
        }
        else {
            modal.find("#inputLogin").removeAttr("disabled");
            modal.find("#inputPassword").removeAttr("disabled");
            modal.find("#inputPassword").val("");
        }
        modal.find("#saveButton").off();
        modal.find("#saveButton").click(function () {
            self.SaveUser(item);
        });

        modal.modal();
    };

    self.DeleteUser = function (item) {
        var warning = $("#myWarning");
        warning.find("#warningBody").html("Удалить пользователя: <strong>" + item.Name() + "</strong>?");
        warning.find("#deleteButton").off();
        warning.find("#deleteButton").click(function () {
            warning.find("#deleteButton").off();
            $.ajax(
                {
                    method: "DELETE",
                    url: "/users/" + item.Id()
                }).done(function (data) {
                    if (data.result === true) {
                        self.users.remove(item);
                    }
                    warning.modal("hide");
                });
        });

        warning.modal();
    };
};