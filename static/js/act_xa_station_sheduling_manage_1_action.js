/**
 * Created by artorias on 2018/10/28.
 */
odoo.define('act_xa_station_sheduling_manage_1_action', function (require) {
    'use strict';

    var Widget = require('web.Widget');
    var core = require('web.core');

    var act_xa_station_sheduling_manage_1_action = Widget.extend({
        init: function (parent, record, node) {
            console.log(record.params.show_data)
            this._super(parent, record, node);
            this.vue_data=record.params.show_data;

        },

//        willStart: function(){
//            var self = this;
//            return self._rpc({
//                model: 'funenc_xa_station.sheduling_manage',
//                method: '',
//                kwargs: '',
//            }).then(function(data){
//                self.vue_data = data
//            })
//
//        },
        start: function () {
            var self = this;
            self._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: {
                    module_name: 'funenc_xa_station',
                    template_name: 'tem_xa_station_sheduling_manage_1_action'
                }
            }).then(function (el) {
                self.replaceElement($(el));
                new Vue({
                    el: '#app',
                    data() {
                        return self.vue_data
                    },
                    methods: {
                        save: function () {
                            var this_vue = this;
                            console.log(self.vue_data);
//                             执行保存操作
                             self._rpc({
                                 model: 'funenc_xa_station.sheduling_manage',
                                 method: 'save_change_data',
                                 kwargs: {kw: self.vue_data}
                             }).then(function (data) {
                                 this_vue.$message({
                                     message: data.message || '恭喜你，这是一条成功消息',
                                     type: 'success'
                                 });
                             })
                        },

                        change_data: function($event,data){
//                            alert(data.id)
                            console.log($event);
                        },

                    }
                })
            })
        }
    });
    core.action_registry.add('act_xa_station_sheduling_manage_1_action', act_xa_station_sheduling_manage_1_action);
    return {act_xa_station_sheduling_manage_1_action: act_xa_station_sheduling_manage_1_action}
});