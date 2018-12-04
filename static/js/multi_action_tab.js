odoo.define("multi_action_tab", function (require) {
    "use strict";

    ///
    // domain 格式 [[["departments", "=", id]]]
    ///
//  alert(111)

    var Widget = require("web.Widget");
    var widgetRegistry = require('web.widget_registry');
    var pyeval = require('web.pyeval');
    var core = require('web.core');

    var g_tab_id = 12345

    function get_group_tab(self, action_id) {
        return self._rpc({
            model: 'funenc_xa_station.return.view.function',
            method: 'return_tab_with_group',
            args: [self.tabs, action_id]
        })
    }

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
            this.action_id = action_descript.context.params.action;
//            clear_breadcrumbs = {clear_breadcrumbs: true};
//            alert(widget_type)
            if (widget_type == 'top') {
                this.options = pyeval.eval('context',
                    action_descript.top_widget_options)
            } else {
                this.options = pyeval.eval('context',
                    action_descript.bottom_widget_options)
            }
            this.tabs = this.options.tabs
        },
        renderElement: function () {
            var self = this;
            $.when(get_group_tab(this, this.action_id)).then(function (data) {
                var $el;
                self.tabs = data;
                if (self.template) {
                    $el = $(core.qweb.render(self.template, {widget: self}).trim());
                } else {
                    $el = self._make_descriptive();
                }
                self.replaceElement($el);
            })
        },

        start: function () {
            var self = this

            this.tabs = self.tabs;
            setTimeout(function () {
                layui.use('element', function () {
                    var element = layui.element;
                    element.on('tab(' + self.tab_id + ")", function (data) {
                        var tab = $(this);
                        if (tab.attr('action')) {
                            self.do_action(tab.attr('action'),{clear_breadcrumbs: true}),
                            console.log(tab.attr('action'),'66666')

                        } else if (tab.attr('action2')) {
                            self.do_action(tab.attr('action2'),{clear_breadcrumbs: true})
                            console.log(tab.attr('action2'),'66666')

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
            })
        }
    });

    widgetRegistry.add("multi_action_tab", multi_action_tab);

    return {
        multi_action_tab: multi_action_tab
    };
});
