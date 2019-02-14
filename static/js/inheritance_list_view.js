odoo.define('inheritance_list_view', function (require) {
    'use strict';

    var ListController = require('web.ListController');


    ListController.include({
        init: function (parent, model, renderer, params) {
            var self = this;
            self._super(parent, model, renderer, params)
        },
        willStart: function () {
            var self = this;
            var get_groups_id = self._rpc({
                model: 'funenc_xa_station.return.view.function',
                method: 'get_groups_with_id'
            });
            return $.when(get_groups_id).then(function (data) {
                self.button_groups_data = data
            })
        }
    })

})