odoo.define('belong_to_management', function (require) {
    "use strict";
    var core = require('web.core');
    var Widget = require('web.Widget');

    var construct_id = 12345124;

    var belong_to_management = Widget.extend({
        app: undefined,
        group_id: 0,
        is_update: false,
        dom_id: 'belong_to_management' + construct_id++,
        init: function (parent, action) {
            var self = this;
            this._super.apply(this, arguments);
            self.group_id = action.context.group_id;
            self.user_data = [];
            self.user_line = [];
            self.user_site = [];   // 部门初始化变量
            if (self.group_id) {
                self.is_update = true
            }
        },

        start: function () {
            var self = this;

            $.when(self._rpc({
                model: 'funenc_xa_station.belong_to_summary',
                method: 'belong_to_method'

            }), self._rpc({
                model: 'funenc_xa_station.belong_to_summary',
                method: 'add_count_line'

            }), self._rpc({
                model: 'funenc_xa_station.belong_to_summary',
                method: 'add_count_site'

            }), this._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: {module_name: 'funenc_xa_station', template_name: 'belong_to_management'}
            })).then(function (user_data, user_line, user_site, res) {
                self.user_data = user_data;
                self.user_line = user_line;
                self.user_site = user_site;
                self.replaceElement($(res));
                var vue = new Vue({
                    el: '#belong_to_management',
                    data() {
                        return {
                            tableData: self.user_data,
                            linei: '',
                            site: '',
                            lines: self.user_line,
                            sites: '',
                            person: '',
                            datetime: '时间选择',
                            input: '',

                        };
                    },

                    methods: {

//                            currentSel: function(){
//                                 return{
//                                 sites: self.user_site,
//                                 };
//                            },

                        search_line_data: function (line_value) {

                            if (vue.lines != '') {
                                self._rpc({
                                    model: 'funenc_xa_station.belong_to_summary',
                                    method: 'search_site',
                                    kwargs: {date: line_value}
                                }).then(function (data) {
                                    vue.sites = data;
                                });

                            }
                            ;

                        },

//                              search_site_data: function(site_value){
//
//                                if (vue.lines != ''){
//                                self._rpc({
//                                           model: 'funenc_xa_station.belong_to_summary',
//                                           method:'search_record',
//                                           kwargs: {date: site_value}
//                                                }).then(function(data){
//                                                      vue.tableData =data;
//                                                    });
//
//                                                 };
//
//                              },

                        search_person_data: function (site_value) {

                            if (vue.lines != '') {
                                self._rpc({
                                    model: 'funenc_xa_station.belong_to_summary',
                                    method: '',
                                    kwargs: {date: site_value}
                                }).then(function (data) {
                                    vue.tableData = data;
                                });

                            }
                            ;

                        },


                        search_data_record: function () {

                            if (vue.datetime != '时间选择') {
                                self._rpc({
                                    model: 'funenc_xa_station.belong_to_summary',
                                    method: 'search_date_record_now',
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


                        // 单击节点
//                            add_record: function(){
//
//                                    self.do_action({
//                                                name: '&#22791;&#29992;&#37329;&#31649;&#29702',
//                                                type: 'ir.actions.act_window',
//                                                res_model: 'funenc_xa_station.reserver_management',
//                                                views: [[false, 'form']],
//                                                method:'add_record',
//                                                target:"new"
//                                            });

//                              },
//                          修改数据
//                            onchange_data: function(index, row){
//                                    self.do_action({
//                                                type: 'ir.actions.act_window',
//                                                res_model: 'funenc_xa_station.belong_to_summary',
//                                                res_id: row['id'],
//                                                views: [[false, 'form']],
//                                            });
//
//                              },


                            onchange_data: function(){
                                if (vue.datetime != '时间选择'){
                                self._rpc({
                                           model: 'funenc_xa_station.belong_to_summary',
                                           method:'search_details_button',
                                           kwargs: {date: vue.datetime,
                                                    line:vue.linei,
                                                    site:vue.site,
                                                    person_id:vue.input}
                                                }).then(function(data){
                                                      self.do_action(data);
                                                    });

                                                };

                              },

                         import_excel_belong_to_management(){
                             if (this.tableData){
                            var url='/funenc_xa_station/belong_to_management_import';
                            var params= {"reserves":this.tableData};
                            var params1=JSON.stringify(params);
                            var oReq = new XMLHttpRequest();
                            oReq.open("POST", url, true);
                            oReq.responseType = "arraybuffer";
                            oReq.onload = function(oEvent) {
                              if (oReq.readyState == 4 && oReq.status == 200) {
                                var blob = new Blob([oReq.response], { type: "application/vnd.ms-excel" });
                                // 转换完成，创建一个a标签用于下载
                                var a = document.createElement('a');
                                //点击事件
                                var evt = document.createEvent("HTMLEvents");
                                evt.initEvent("click", false, false);
                                // 设置文件名
                                a.download = '属地检查汇总'+(new Date()).getTime();
                                // 利用URL.createObjectURL()方法为a元素生成blob URL
                                a.href = URL.createObjectURL(blob);
                                a.click();
                              }
                            };

                            oReq.send(params1);
                          }
                         },

                        onchange_data: function (index, row) {
                            self.do_action({
                                type: 'ir.actions.act_window',
                                res_model: 'funenc_xa_station.belong_to_summary',
                                res_id: row['id'],
                                views: [[false, 'form']],
                                target: "new"
                            });

                        },
                        import_excel_belong_to_management() {
                            if (this.tableData) {
                                var url = '/funenc_xa_station/belong_to_management_import';
                                var params = {"reserves": this.tableData};
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
                                        a.download = '属地检查汇总' + (new Date()).getTime();
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

    core.action_registry.add('belong_to_management', belong_to_management);
    return {'belong_to_management': belong_to_management};


});
