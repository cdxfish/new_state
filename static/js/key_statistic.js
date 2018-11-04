odoo.define('key_statistic', function (require) {
    "use strict";
    var core = require('web.core');
    var Widget = require('web.Widget');

    var construct_id = 123456;

    var key_statistic = Widget.extend({
        app: undefined,
        group_id: 0,
        is_update: false,
        dom_id: 'key_statistic' + construct_id++,
        init: function (parent, action) {
            var self = this;
            this._super.apply(this, arguments);
            self.group_id = action.context.group_id;
            self.key_data = { "result": [] };   // 声明钥匙统计变量
            self.key_views_ids = { "result": [] }; // 声明view 变量  用来 明确跳转
            if (self.group_id) {
                self.is_update = true
            }
        },
        start: function () {
            var self = this;
            $.when(self._rpc({
                model: 'funenc.xa.station.key.manage',
                method: 'get_statistic_key_data'
            }), self._rpc({
                model: 'funenc.xa.station.key.manage',
                method: 'get_key_view_ids'

            }), self._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: { module_name: 'funenc_xa_station', template_name: 'key_statistic' }
            })).then(function (key_data, key_views_ids, res) {
                self.key_data = key_data;
                self.key_views_ids = key_views_ids;
                self.replaceElement($(res));
                new Vue({
                    el: '#funenc_xa_station',
                    data() {
                        return {
                            line: '',
                            lines: [],
                            station: '',
                            stations: [],
                            key: '',
                            keys: [], 
                            total: 130, // 数据总数，用于分页，默认20条记录每页
                            currentPage: 1, // 当前页数，默认1
                            tableData: self.key_data

                        };
                    },

                    methods: {
                        onSubmit: function(){

                        },
                        handleCurrentChange: function(){
                            console.log(this.currentPage)
                        },
                        details: function(row){
                                   self._rpc({
                                    model: 'funenc.xa.station.key.detail',
                                    method: 'browse_key_details',
                                    kwargs:{'line_id':row.line_id,
                                            'site_id':row.site_id,
                                            'key_type':row.key_type,
                                            'key_total':row.key_total,
                                            'master_number':row.master_number,
                                            'copy_number':row.copy_number,
                                            'borrow_number':row.borrow_number,
                                            'destroy_number':row.destroy_number}
                                    }).then(function(data) {
                                            self.do_action(data);
                                        });
                        },
                        // 钥匙创建
                        create_key: function () {

                            self.do_action({
                                name: '\u94a5\u5319\u65b0\u5efa',
                                type: 'ir.actions.act_window',
                                res_model: 'funenc.xa.station.key.detail',
                                views: [[false, 'form']],
                                target: 'new'
                            });


                        },

                        // 钥匙借用

                        key_borrow_record: function () {

                            self.do_action({
                                name: '\u94a5\u5319\u501f\u7528',
                                type: 'ir.actions.act_window',
                                res_model: 'funenc.xa.station.borrow.record',
                                views: [[self.key_views_ids['borrow_record_form_1'], 'form']],
                                target: 'new',
                                context: self.key_views_ids['context']
                            });


                        },

                        // 钥匙归还

                        key_return: function () {

                            self.do_action({
                                name: '\u94a5\u5319\u5f52\u8fd8',
                                type: 'ir.actions.act_window',
                                res_model: 'funenc.xa.station.borrow.record',
                                views: [[self.key_views_ids['borrow_record_form'], 'form']],
                                target: 'new',
                                context: { 'active_model': 'funenc.xa.station.borrow.record' }
                            });


                        },

                        // 钥匙借用记录

                        key_borrow_record_list: function () {

                            self.do_action({
                                name: '\u94a5\u5319\u501f\u7528\u8bb0\u5f55',
                                type: 'ir.actions.act_window',
                                res_model: 'funenc.xa.station.borrow.record',
                                views: [[self.key_views_ids['borrow_record_list'], 'list'], [self.key_views_ids['borrow_record_form'], 'form']],
                                target: 'current',
                            });
                        },
                    }
                });
            })
        }
    });

    core.action_registry.add('key_statistic', key_statistic);
    return { 'key_statistic': key_statistic };


});
