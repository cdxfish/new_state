odoo.define("no_open_tree", function(require) {
  "use strict";
  var core = require("web.core");
  var session = require("web.session");
  var ListRenderer = require("web.ListRenderer");

  ListRenderer.include({
    _onRowClicked: function(event) {
      if (this.$el[0].className.indexOf("noOpen") == 0) {
        return false;
      }
      if (!$(event.target).prop("special_click")) {
        var id = $(event.currentTarget).data("id");
        if (id) {
          this.trigger_up("open_record", { id: id, target: event.target });
        }
      }
    }
  });
});