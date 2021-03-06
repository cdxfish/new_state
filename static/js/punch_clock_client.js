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
                self = this;
                this.vue_data = {
                    days: ['9-1', '9-2'],
                    month: new Date(),
                    line_options: [],

                    station_options: [],
                    sel_user: [],
                    user_options: [],
                    loading: false,
                    attendance_table_data: '',
                    attendance_total_table_data: [{
                    user_name: '',
                    work_num: '',
                    position: '',
                    total_work_time: '',
                    no_work_time: '',
                    night_work_time: '',
                    add_work_time: '',
                    sick_leave: '',
                    maternity_leave: '',
                    compassionate_leave: '',
                    year_leave: '',
                    marry_leave: '',
                    maternited_leave: '',
                    nursing_leave: '',
                    funeral_leave: '',
                    job_injury_leave: '',
                    absenteeism: ''
                    }]
                };
            },
            willStart: function () {

                    var self= this;
                    return self._rpc({
                        model: 'fuenc_station.clock_record',
                        method: 'get_clock_record_date',
                    }).then(function(data){
                        self.vue_data.line_options = data.line_options;
                        self.vue_data.station_options = data.site_options;
                        self.vue_data.sel_line = data.line_id;
                        self.vue_data.sel_station = data.site_id;
                        self.vue_data.user_options = data.default_users;
                        self.vue_data.days = data.default_data.days;
                        self.vue_data.attendance_table_data = data.default_data.attendance_table_data;
                        self.vue_data.attendance_total_table_data = data.default_data.attendance_total_table_data;


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
                                        self.vue_data.station_options = data
                                    })

                                },

                                select_user:function(site_id){

                                     self._rpc({
                                        model: 'cdtct_dingtalk.cdtct_dingtalk_department',
                                        method: 'pc_get_users_by_department_id',
                                        kwargs: {site_id: site_id}
                                    }).then(function(data){
                                        self.vue_data.user_options = data
                                    })

                                },

                                search: function () {

                                    self._rpc({
                                             model: 'fuenc_station.clock_record',
                                             method: 'get_clock_record',
                                             kwargs: {start_time: self.vue_data.month.getTime(),
                                                      site_id: self.vue_data.sel_station,
                                                      user_id: self.vue_data.sel_user,
                                                      line_id: self.vue_data.sel_line
                                             }
                                         }).then(function (data) {
                                             self.vue_data.days = data.days;
                                             self.vue_data.attendance_table_data = data.attendance_table_data;
                                             self.vue_data.attendance_total_table_data = data.attendance_total_table_data;
                                         })


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