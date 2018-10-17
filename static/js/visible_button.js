odoo.define('btn_display_widget', function (require) {
    "use strict";

        var core = require('web.core');
        var Widget = require('web.Widget');
        var widget_registry = require('web.widget_registry');

     console.log('222')

    var btn_display_widget = Widget.extend({
        init: function (parent,record) {
         console.log('333')
//            this._super.apply(this,arguments);
//
            console.log('record',record);

            self.record=record;
        },
        start: function () {
            var self = this;

            var html='<div class="layui-btn-group">';
            html += '<button class="layui-btn layui-btn-sm" type="object" name="edit" id="id_1" style="display:none">编辑</button>';

            html += '<button class="layui-btn layui-btn-sm layui-btn-danger" type="object" name="delete" confirm="您确定要删除该钥匙类型吗？" >删除</button>';
            html +='</div>';
            this.$el.html(html);

            this.$el.find('#id_1').click(function(){
                console.log('click')

            })

        },
        _render: function () {
            if (this.mode === 'edit') {
                return this._renderEdit();
            } else if (this.mode === 'readonly') {
                return this._renderReadonly();
            }
        },
    });

    widget_registry.add('btn_display_widget', btn_display_widget);
    return {btn_display_widget: btn_display_widget}
});