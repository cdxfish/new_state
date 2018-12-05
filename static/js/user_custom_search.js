odoo.define('UserCustomSearch', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var widgetRegistry = require('web.widget_registry');

    var UserCustomSearch = Widget.extend({
        template: 'group_user_search',
        events: {
            'click .do_search': 'on_search_click',
        },

        on_search_click: function () {
            var name = this.$('.user_name').val()
            var domain = []
            if (name != '') {
                domain.push(['name', 'like', name])
            }
            this.trigger_up('custom_search_apply', {
                domain: domain
            })
        }
    })

    // 注册搜索
    widgetRegistry.add('UserCustomSearch', UserCustomSearch)

    return {
        UserCustomSearch: UserCustomSearch
    }
});