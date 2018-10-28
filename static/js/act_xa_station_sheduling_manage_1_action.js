/**
 * Created by artorias on 2018/10/28.
 */
odoo.define('act_xa_station_sheduling_manage_1_action', function (require) {
    'use strict';

    var Widget = require('web.Widget');
    var core = require('web.core');

    var act_xa_station_sheduling_manage_1_action = Widget.extend({
        init: function (parent, record, node) {
            this._super(parent, record, node);
            this.vue_data = {
                days: ['9月2日', '9月3日', '9月4日', '9月5日', '9月6日', '9月7日'],
                // shift_value里字典的个数需要与days的元素个数相对应
                group_table_data: [{
                    group_name: 'A1',
                    user_name: '王小虎',
                    work_number: '109912',
                    position: '站长',
                    shift_value: [
                        {id: '1', shift: 'day'}, {id: '2', shift: 'night'}, {id: '1', shift: 'day'},
                        {id: '1', shift: 'day'}, {id: '1', shift: 'day'}, {id: '1', shift: 'day'},
                        {id: '1', shift: 'day'}
                    ]
                }, {
                    group_name: 'A1',
                    user_name: '王小虎',
                    work_number: '109912',
                    position: '站长12',
                    shift_value: [
                        {id: '', shift: ''}, {id: '', shift: ''}, {id: '', shift: ''},
                        {id: '', shift: ''}, {id: '', shift: ''}, {id: '', shift: ''},
                        {id: '', shift: ''}
                    ]
                }, {
                    group_name: 'A1',
                    user_name: '王小虎',
                    work_number: '109912',
                    position: '站长',
                    shift_value: [
                        {id: '', shift: ''}, {id: '', shift: ''}, {id: '', shift: ''},
                        {id: '', shift: ''}, {id: '', shift: ''}, {id: '', shift: ''},
                        {id: '', shift: ''}
                    ]
                }, {
                    group_name: 'A1',
                    user_name: '王小虎',
                    work_number: '109912',
                    position: '站长',
                    shift_value: [
                        {id: '', shift: ''}, {id: '', shift: ''}, {id: '', shift: ''},
                        {id: '', shift: ''}, {id: '', shift: ''}, {id: '', shift: ''},
                        {id: '', shift: ''}
                    ]
                }],

                motorized_group_table_data: [{
                    user_name: '王小虎',
                    work_number: '109912',
                    position: '站长',
                    shift_value: [
                        {id: '1', shift: 'day'}, {id: '2', shift: 'night'}, {id: '1', shift: 'day'},
                        {id: '1', shift: 'day'}, {id: '1', shift: 'day'}, {id: '1', shift: 'day'},
                        {id: '1', shift: 'day'}
                    ]
                }, {
                    user_name: '王小虎',
                    work_number: '109912',
                    position: '站长12',
                    shift_value: [
                        {id: '', shift: ''}, {id: '', shift: ''}, {id: '', shift: ''},
                        {id: '', shift: ''}, {id: '', shift: ''}, {id: '', shift: ''},
                        {id: '', shift: ''}
                    ]
                }, {
                    user_name: '王小虎',
                    work_number: '109912',
                    position: '站长',
                    shift_value: [
                        {id: '', shift: ''}, {id: '', shift: ''}, {id: '', shift: ''},
                        {id: '', shift: ''}, {id: '', shift: ''}, {id: '', shift: ''},
                        {id: '', shift: ''}
                    ]
                }, {
                    user_name: '王小虎',
                    work_number: '109912',
                    position: '站长',
                    shift_value: [
                        {id: '', shift: ''}, {id: '', shift: ''}, {id: '', shift: ''},
                        {id: '', shift: ''}, {id: '', shift: ''}, {id: '', shift: ''},
                        {id: '', shift: ''}
                    ]
                }],

                total_group_table_data: [
                    {
                        group_name: '白班', shift_value: [
                            {user_number: '10'}, {user_number: '20'}, {user_number: '13'}, {user_number: '16'},
                            {user_number: '20'}, {user_number: '14'}, {user_number: '21'}
                        ]
                    },
                    {
                        group_name: '夜班', shift_value: [
                            {user_number: '11'}, {user_number: '20'}, {user_number: '13'}, {user_number: '16'},
                            {user_number: '20'}, {user_number: '15'}, {user_number: '21'}
                        ]
                    }
                ],


                shift_options: [{
                    value: 'day',
                    label: '白'
                }, {
                    value: 'night',
                    label: '夜'
                }, {
                    value: 'all_day',
                    label: '日'
                }, {
                    value: 'no_day',
                    label: '休'
                }],
            }
        },
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
                            // 执行保存操作
                            // self._rpc({
                            //     model: '',
                            //     method: '',
                            //     kwargs: {}
                            // }).then(function (data) {
                            //     this_vue.$message({
                            //         message: data.message || '恭喜你，这是一条成功消息',
                            //         type: 'success'
                            //     });
                            // })
                        }
                    }
                })
            })
        }
    });
    core.action_registry.add('act_xa_station_sheduling_manage_1_action', act_xa_station_sheduling_manage_1_action);
    return {act_xa_station_sheduling_manage_1_action: act_xa_station_sheduling_manage_1_action}
});