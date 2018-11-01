/**
 * Created by artorias on 2018/10/28.
 */
odoo.define('change_shifts_clint', function (require) {
    'use strict';

    var Widget = require('web.Widget');
    var core = require('web.core');

    var change_shifts_clint = Widget.extend({
        init: function (parent, record, node) {
            console.log(record.params.show_data)
            this._super(parent, record, node);
            this.vue_data = {
                    activeName: 'first',
                    shift_shift_data:[
//                    {
//                    index: 1,
//                    shift_shift_date:'2010-10-10',
//                    take_over_user: '张三',
//                    job_no:001,
//                    take_over_date: '2010-10-11'
//                    }
                    ]


                };

        },

//        willStart: function () {
//
//                    var self= this;
//
//                    return self._rpc({
//                        model: 'cdtct_dingtalk.cdtct_dingtalk_department',
//                        method: 'get_line_id',
//                    }).then(function(data){
//                        self.vue_data.line_options = data
//                    })
//            },
        start: function () {
            var self = this;
            self._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: {
                    module_name: 'funenc_xa_station',
                    template_name: 'test_demo'
                }
            }).then(function (el) {
                self.replaceElement($(el));
                new Vue({
                    el: '#app',
                    data() {
                        return self.vue_data
                    },

                    methods: {
                        shift_shift: function(){

                        },

                        take_over: function(){
                            self._rpc({
                                model: 'funenc_xa_station.production_change_shifts',
                                method: 'get_views'

                            }).then(function (data) {
//                                    self.do_action({
//                                                    name: '\u94a5\u5319\u65b0\u5efa',
//                                                    type: 'ir.actions.act_window',
//                                                    res_model: 'funenc_xa_station.production_change_shifts',
//                                                    views: [[data.list_views, 'tree'],[data.form_views,'form']],
//                                                    target: 'new',
//                                                    domain: data.domain
//                                                })
                            });

                        },

                        handleClick(tab, event) {
                            console.log(tab, event);
                        },



                    }
                })
            })
        }
    });
    core.action_registry.add('change_shifts_clint', change_shifts_clint);
    return {change_shifts_clint: change_shifts_clint}
});