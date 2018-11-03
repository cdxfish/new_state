/**
 * Created by artorias on 2018/11/3.
 */
odoo.define('extend_theme_form', function (require) {
    "use strict";

    var FormController = require('web.FormController');

    FormController.include({
        _onSave: function (ev) {
            console.log('_onsave')
            var self = this;
            ev.stopPropagation(); // Prevent x2m lines to be auto-saved
            this.saveRecord().then(function () {
                self.trigger_up('history_back');
            })
        }
    })
});