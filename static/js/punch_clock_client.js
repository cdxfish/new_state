/**
 * Created by artorias on 2018/10/29.
 */
odoo.define('punch_clock_client', function (require) {
    'use strict';

    var Widget = require('web.Widget');
    var core = require('web.core');

    var punch_clock_client = Widget.extend({
            init: function (parent, record, node) {
                this._super(parent, record, node);
                this.vue_data = {
                    days: ['9-1', '9-2'],
                    sel_date: '',
                    sel_line: '',
                    month: '',
                    sel_station: '',
                    line_options: [{
                        value: '选项1',
                        label: '黄金糕'
                    }, {
                        value: '选项2',
                        label: '双皮奶'
                    }, {
                        value: '选项3',
                        label: '蚵仔煎'
                    }, {
                        value: '选项4',
                        label: '龙须面'
                    }, {
                        value: '选项5',
                        label: '北京烤鸭'
                    }],

                    station_options: [{
                        value: '选项1',
                        label: '黄金糕'
                    }, {
                        value: '选项2',
                        label: '双皮奶'
                    }, {
                        value: '选项3',
                        label: '蚵仔煎'
                    }, {
                        value: '选项4',
                        label: '龙须面'
                    }, {
                        value: '选项5',
                        label: '北京烤鸭'
                    }],
                    sel_user: '',
                    user_options: [],
                    loading: false,
                    attendance_table_data: '',
                    attendance_total_table_data: [{
                        user_name: '张三',
                        work_num: '92323',
                        position: '站长',
                        total_work_time: '23',
                        no_work_time: '1',
                        night_work_time: '3',
                        add_work_time: '34',
                        sick_leave: '1223',
                        maternity_leave: '1',
                        compassionate_leave: '23',
                        year_leave: '55',
                        marry_leave: '1242',
                        maternited_leave: '55',
                        nursing_leave: '10',
                        funeral_leave: '98',
                        job_injury_leave: '87',
                        absenteeism: 76
                    }]
                };
            },
            willStart: function () {

                    var self= this;

                    return self._rpc({
                        model: 'cdtct_dingtalk.cdtct_dingtalk_department',
                        method: 'get_line_id',
                    }).then(function(data){
                        self.vue_data.line_options = data
                    })
            },
            start: function () {
                var self = this;
                setTimeout(function () {
                    self._rpc({
                        model: 'vue_template_manager.template_manage',
                        method: 'get_template_content',
                        kwargs: {module_name: 'funenc_xa_station', template_name: 'punch_clock_client'}
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
//                                that._rpc({
//                                    model: 'cdtct_dingtalk.cdtct_dingtalk_department',
//                                    method: 'get_line_id',
//                                }).then(function(data){
//                                    that.vue_data.lines = data
//                                })
//
//                            },

                            methods: {
                                remoteMethod(query) {
                                    if (query !== '') {
                                        this.loading = true;
                                        // setTimeout(() => {
                                        //     this.loading = false;
                                        //     self._rpc({
                                        //         model: '',
                                        //         method: '',
                                        //         kwargs: {}
                                        //     }).then(function (data) {
                                        //         self.vue_data.user_options = data
                                        //     })
                                        // }, 200);
                                        this.loading = false;
                                        self.vue_data.user_options = [{label: '张三', id: '1'}]
                                    } else {
                                        self.vue_data.user_options = [];
                                    }
                                },

                                select_line:function(line_id){

                                     self._rpc({
                                        model: 'cdtct_dingtalk.cdtct_dingtalk_department',
                                        method: 'get_sites',
                                        kwargs: {line_id: line_id}
                                    }).then(function(data){
                                        console.log(data)
                                        self.vue_data.station_options = data
                                    })

                                },

                                select_user:function(site_id){

                                     self._rpc({
                                        model: 'cdtct_dingtalk.cdtct_dingtalk_department',
                                        method: 'pc_get_users_by_department_id',
                                        kwargs: {site_id: site_id}
                                    }).then(function(data){
                                        console.log(data)
                                        self.vue_data.user_options = data
                                    })

                                },

                                search: function () {
                                if (self.vue_data.month && self.vue_data.sel_station){

                                    self._rpc({
                                             model: 'fuenc_station.clock_record',
                                             method: 'get_clock_record',
                                             kwargs: {start_time: self.vue_data.month,
                                                      site_id: self.vue_data.sel_station,
                                                      user_id: self.vue_data.sel_user
                                             }
                                         }).then(function (data) {
                                             self.vue_data.days = data.days;
                                             self.vue_data.attendance_table_data = data.attendance_table_data;
                                             self.vue_data.attendance_total_table_data = data.attendance_total_table_data;
                                         })
                                    }


                                }
                            }
                        })
                    })
                })
            }
        })
    ;
    core.action_registry.add('punch_clock_client', punch_clock_client);
    return {punch_clock_client: punch_clock_client}
})
;