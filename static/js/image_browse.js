odoo.define('image_browse', function (require) {
    "use strict";

//    var Widget = require('web.Widget');
//    var widget_registry = require('web.widget_registry');

    var AbstractField = require('web.AbstractField');
    var config = require('web.config');
    var core = require('web.core');
    var datepicker = require('web.datepicker');
    var Domain = require('web.Domain');
    var DomainSelector = require('web.DomainSelector');
    var DomainSelectorDialog = require('web.DomainSelectorDialog');
    var framework = require('web.framework');
    var session = require('web.session');
    var utils = require('web.utils');
    var view_dialogs = require('web.view_dialogs');
    var field_registry = require('web.field_registry');


    var value_to_str_widget = AbstractField.extend({
        init: function () {
            this._super.apply(this,arguments);
            this.lunchData  =  JSON.parse(this.value);

        },
        start: function () {
            var self = this;
            if (self.value) {
                this.$el.html();
            }
            this.$el.css('text-align','center;')
        },
        _render: function () {
            if (this.mode === 'edit') {
                return this._renderEdit();
            } else if (this.mode === 'readonly') {
                return this._renderReadonly();
            }
        },
    });

    field_registry.add('value_to_str_widget', value_to_str_widget);
    return {value_to_str_widget: value_to_str_widget}
});