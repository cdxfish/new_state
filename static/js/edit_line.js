odoo.define("chart_view", function(require) {
  "use strict";

  var core = require("web.core");
  var Widget = require("web.Widget");

  var chart_view = Widget.extend({
    renderElement: function() {
      var $el = $('<div id="editLine"></div>');
      this.replaceElement($el);
    },
    start: function() {
      var self = this;
      Vue.config.productionTip = false;
      Vue.nextTick(function() {
        g_init_edit_line(self);
      });
    }
  });

  core.action_registry.add("chart_view", chart_view);

  return {
    chart_view: chart_view
  };
});
