/**
 * Created by artorias on 2018/10/29.
 */
odoo.define('scheduling_summary', function (require) {
    'use strict';

    var Widget = require('web.Widget');
    var core = require('web.core');

    var scheduling_summary = Widget.extend({
            init: function (parent, record, node) {
                this._super(parent, record, node);

                self = this;
                this.vue_data = {
                    height: '800px',
                    month: new Date(),
                    arrange_orders: [],
                    days: [],
                    // shift_value里字典的个数需要与days的元素个数相对应
                    day_table_data: [],
                    total_table_data: [],
                    line_options:[],
                    site_options:[],
                    lines:'',
                    sites:'',
                };
            },
            willStart: function(){
                    var self = this;
                    return self._rpc({
                        model: 'cdtct_dingtalk.cdtct_dingtalk_department',
                        method: 'get_default_sheduling_data',
                    }).then(function(data){
                        console.log(data)
                        self.vue_data.arrange_orders = data['arrange_orders'];
                        self.vue_data.days = data['days'];
                        self.vue_data.day_table_data = data['day_table_data'];
                        self.vue_data.total_table_data = data['total_table_data'];
                        self.vue_data.line_options = data['line_options'];
                        self.vue_data.site_options = data['site_options'];
                        self.vue_data.lines = data['default_line'];
                        self.vue_data.sites = data['default_site'];
                    });
                },
            start: function () {
                var self = this;

                setTimeout(function () {
                    self._rpc({
                        model: 'vue_template_manager.template_manage',
                        method: 'get_template_content',
                        kwargs: {module_name: 'funenc_xa_station', template_name: 'scheduling_summary'}
                    }).then(function (el) {
                        self.replaceElement($(el));
                        new Vue({
                            el: '#app',
                            data() {
                                return self.vue_data
                            },
//                            mounted() {
//                                var that = this;
//                                var height = window.innerHeight - 20;
//                                that.height = "padding:40px 80px;height: " + height + "px;";
//                                self._rpc({
//                                    model: 'cdtct_dingtalk.cdtct_dingtalk_department',
//                                    method: 'get_line_id',
//                                }).then(function(data){
//                                    self.vue_data.line_options = data
//                                })



//                            },
                            methods: {
                                //线路change事件
                            selectLine(val) {
                               self._rpc({
                                    model: 'cdtct_dingtalk.cdtct_dingtalk_department',
                                    method: 'get_sites',
                                    kwargs: {line_id: val}
                                }).then(function(data){
                                    self.vue_data.site_options = data
                                })
                            },
                            //查询事件
                            onSubmit() {

                               if (this.month && this.sites){
                                self._rpc({
                                    model: 'funenc_xa_station.sheduling_manage',
                                    method: 'get_cline_data',
                                    kwargs: {site_id:this.sites,start_time:this.month}
                                }).then(function(data){
                                    self.vue_data.days = data['days'];
                                    self.vue_data.day_table_data = data['day_table_data'];
                                    self.vue_data.total_table_data = data['total_table_data'];
                                    self.vue_data.arrange_orders = data['arrange_orders']
                                })
                               }

                            },

                            }
                        })
                    })
                })
            }
        })
    ;
    core.action_registry.add('scheduling_summary', scheduling_summary);
    return {scheduling_summary: scheduling_summary}
})
;