odoo.define('my_mail_thread', function (require) {
"use strict";

var mailThreadField = require('mail.ThreadField');
var core = require('web.core');
var field_registry = require('web.field_registry');
var _t = core._t;

// -----------------------------------------------------------------------------
// 'mail_thread' widget: displays the thread of messages
// -----------------------------------------------------------------------------
var my_mail_thread = mailThreadField.extend({
    // inherited
    init: function (parent, state, params) {
        this.message_id = params.context.active_id;
        this._super(parent, state, params);
    },

    _render: function () {
        // 这里可以传入记录id,在mail_message表中
        // console.log('self=',self.record.context.active_id)
        var self = this;

        this._rpc({
            model: 'funenc_xa_station.operation_log',
            method: 'get_log_ids',
            kwargs: {message_id: this.message_id}
        }).then(function (return_data) {
            self._fetchAndRenderThread(return_data);

        });

    }

});

field_registry.add('my_mail_thread', my_mail_thread);

return my_mail_thread;

});
