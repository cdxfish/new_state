odoo.define('funenc_xa_check', function (require) {
    "use strict";
    var core = require('web.core');
    var Widget = require('web.Widget');

    var construct_id = 121555551;

    var funenc_xa_check = Widget.extend({
        app: undefined,
        group_id: 0,
        is_update: false,
        dom_id: 'funenc_xa_check' + construct_id++,
        init: function (parent, action) {
            var self = this;
            this._super.apply(this, arguments)
            self.group_id = action.context.group_id
            self.date_date =new Date();
            self._rpc({
                model: 'funenc_xa_station.check_collect',
                method: 'get_group_2'
            }).then(function (data) {
//                console.log(data);
                if (data) {
                    self.data_2 = true;
                } else {
                    self.data_2 = false;
                }
                ;
            });
            self.user_line = [];
            self.user_site = [];
            self._rpc({
                model: 'funenc_xa_station.check_collect',
                method: 'get_group_1'
            }).then(function (data) {
//                console.log(data);
                if (data) {
                    self.data_1 = true;
                } else {
                    self.data_1 = false;
                }
                ;
            });

            self._rpc({
                model: 'funenc_xa_station.check_collect',
                method: 'get_group_3'
            }).then(function (data) {
//                console.log(data);
                if (data) {
                    self.data_3 = true;
                } else {
                    self.data_3 = false;
                }
                ;
            });

            self._rpc({
                model: 'funenc_xa_station.check_collect',
                method: 'get_group_4'
            }).then(function (data) {
//                console.log(data);
                if (data) {
                    self.data_4 = true;
                } else {
                    self.data_4 = false;
                }
                ;
            });

            self.user_data = [];   // 部门初始化变量
            if (self.group_id) {
                self.is_update = true
            }
        },

        renderElement: function () {
            var self = this;
            var $el = $('<div id="funenc_xa_check"></div>');
            self.replaceElement($el);
        },

        willStart: function(){
            var self = this;
            return self._rpc({
                model: 'cdtct_dingtalk.cdtct_dingtalk_department',
                method: 'get_default_sheduling_data',
            }).then(function(data){
                  self.line_self = data.default_line;
                  self.site_self = data.default_site;
            });
        },

        start: function () {
            var self = this;
            $.when(self._rpc({
                model: 'funenc_xa_station.check_collect',
                method: 'check_record_method'
            }),

            self._rpc({
                model: 'funenc_xa_station.belong_to_summary',
                method: 'add_count_line'
            }),

            self._rpc({
                model: 'funenc_xa_station.belong_to_summary',
                method: 'add_count_site'

            }),
            this._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: {module_name: 'funenc_xa_station', template_name: 'funenc_xa_check'}
            })).then(function (user_data,user_line, user_site, res) {
                self.user_data = user_data;
                self.user_line = user_line;
                self.user_site = user_site;
                self.replaceElement($(res));
                var vue = new Vue({
                    el: '#funenc_xa_check',
                    data() {
                        return {
                            tableData: self.user_data,
                            value6: '时间选择',
                            tabValue: '',
                            check: '',
                            show_1: self.data_1,
                            show_2: self.data_2,
                            show_3: self.data_3,
                            show_4: self.data_4,
                            linei: self.line_self,
                            site: self.site_self,
                            lines: self.user_line,
                            sites: self.user_site,
                            person: '',
                            datetime:self.date_date,
                            input: '',
                            newdate:'',

                        };
                    },
                    methods: {

                        // 点击进入方法
//                        search_time: function () {
//
//                            if (vue.value6 != '时间选择') {
//                                self._rpc({
//                                    model: 'funenc_xa_station.check_collect',
//                                    method: 'search_record_method',
//                                    kwargs: {date: vue.value6}
//                                }).then(function (data) {
//                                    vue.tableData = data;
//                                });
//
//                            }
//                            ;
//
//                        },

                        search_line_data: function (line_value) {
                            if (vue.lines != '') {
                                self._rpc({
                                    model: 'funenc_xa_station.award_collect',
                                    method: 'search_site',
                                    kwargs: {date: line_value}
                                }).then(function (data) {
                                    vue.sites = data;
                                });

                            }
                            ;

                        },
//                          tab页面的跳转功能
                        handleSelect: function () {
                            var that = this;
//                            console.log(that.tabValue，'34343');
                            if (that.tabValue == 2) {
                                self._rpc({
                                    model: 'funenc_xa_station.check_collect',
                                    method: 'get_action',
                                    group: 'funenc_xa_station.table_evaluation_total'
                                }).then(function (data) {
                                    self.do_action(data);
                                    that.check = data.user_id;
//                                                                            console.log('999999999',that.check);

                                });

                            } else if (that.tabValue == 4) {
                                self._rpc({
                                    model: 'funenc_xa_station.award_collect',
                                    method: 'get_action',
                                }).then(function (data) {
//                                                                        console.log(data);
                                    self.do_action(data);
                                });


                            } else if (that.tabValue == 1) {
                                self._rpc({
                                    model: 'funenc_xa_station.check_record',
                                    method: 'get_action',
                                }).then(function (data) {
                                    self.do_action(data);

                                });
                            } else if (that.tabValue == 3) {
                                self._rpc({
                                    model: 'funenc_xa_station.award_record',
                                    method: 'get_action',
                                }).then(function (data) {
                                    self.do_action(data);
                                });

                            }
                        },

                        search_data_record: function () {
                            if (vue.datetime != '时间选择') {
                                self._rpc({
                                    model: 'funenc_xa_station.check_collect',
                                    method: 'search_record_method',
                                    kwargs: {
                                        date: vue.datetime,
                                        line: vue.linei,
                                        site: vue.site,
                                        person_id: vue.input
                                    }
                                }).then(function (data) {
                                    vue.tableData = data;
                                });

                            }
                            ;

                        },

                        import_excel() {
                            if (this.tableData) {
                                var url = '/fuenc_xa_station/collect_download';
                                var params = {"exl_data": this.tableData};
                                var params1 = JSON.stringify(params);
                                var oReq = new XMLHttpRequest();
                                oReq.open("POST", url, true);
                                oReq.responseType = "arraybuffer";
                                oReq.onload = function (oEvent) {
                                    if (oReq.readyState == 4 && oReq.status == 200) {
                                        var blob = new Blob([oReq.response], {type: "application/vnd.ms-excel"});
                                        // 转换完成，创建一个a标签用于下载
                                        var a = document.createElement('a');
                                        //点击事件
                                        var evt = document.createEvent("HTMLEvents");
                                        evt.initEvent("click", false, false);
                                        // 设置文件名
                                        a.download = '考评汇总' + (new Date()).getTime();
                                        // 利用URL.createObjectURL()方法为a元素生成blob URL
                                        a.href = URL.createObjectURL(blob);
                                        a.click();
                                    }
                                };

                                oReq.send(params1);
                            }
                        },


                    },

                });
            })
        },


    });

    core.action_registry.add('funenc_xa_check', funenc_xa_check);
    return {'funenc_xa_check': funenc_xa_check};


});
