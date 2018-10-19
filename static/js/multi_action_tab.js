odoo.define("multi_action_tab", function (require) {
  "use strict";

  ///
  // domain 格式 [[["departments", "=", id]]]
  ///
//  alert(111)

  var Widget = require("web.Widget");
  var widgetRegistry = require('web.widget_registry');
  var pyeval = require('web.pyeval');

  var g_tab_id = 12345

  var multi_action_tab = Widget.extend({
    action_manager: undefined,
    action_descript: '',
    control_pannel: undefined,
    widget_type: 'top',
    tab_id: 'lay_tab_' + g_tab_id++,
    tabs: [],
    template: 'layui_window_tab',
    init: function (parent, widget_type, action_manager, action_descript) {
      this._super.apply(this, arguments)

      this.widget_type = widget_type
      this.control_pannel = parent
      this.action_manager = action_manager
      this.action_descript = action_descript
//            alert(widget_type)
      console.log("widget_type:"+widget_type)
      if (widget_type == 'top') {
        this.options = pyeval.eval('context',
          action_descript.top_widget_options)
      } else {
        this.options = pyeval.eval('context',
          action_descript.bottom_widget_options)
      }

      this.tabs = this.options.tabs
    },

    start: function () {
      var self = this
      self.$el.addClass("layui-tab-brief")

      this.tabs=self.tabs;

      layui.use('element', function () {
        var element = layui.element;
        console.log('element:'+element)
        element.on('tab(' + self.tab_id + ")", function (data) {
          var index = data.index
            console.log('index:'+index)
          var tab = self.tabs[index]
          console.log(JSON.stringify(tab))

          if (tab.action) {
            self.do_action(tab.action)

          } else if (tab.action2) {
            self.do_action(tab.action2)
//          console.log("domains:"+JSON.stringify(tab.domains))
//
//            var inner_widget = self.action_manager.inner_widget
//            console.log("inner_widget:"+inner_widget)
//            if (inner_widget) {
//              var user_context = self.getSession().user_context;
//              console.log("user_context:"+user_context)
//              inner_widget.trigger_up("search", {
//                domains: [tab.domains],
//                contexts: user_context,
//                groupbys: []
//              });
//            }
          } else {
            console.log('yu must set the action or the domain in the option');
          }
        });
      });
    }
  });

  widgetRegistry.add("multi_action_tab", multi_action_tab);

  return {
    multi_action_tab: multi_action_tab
  };
});
