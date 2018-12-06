odoo.define('good_deeds_summary', function (require) {
    "use strict";
    var core = require('web.core');
    var Widget = require('web.Widget');


    var good_deeds_summary = Widget.extend({
        init: function (parent, action) {
            var self = this;
            this._super.apply(this, arguments);
            self.date_self = new Date();
        },
        start: function () {
            var self = this;

            $.when(
            self._rpc({
                       model:'funenc_xa_station.good_deeds_summary',
                       method:'init_methods_action',
                    }),
            self._rpc({
                        model: 'funenc_xa_station.good_deeds_summary',
                        method: 'get_department',
                    }),
            this._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: {module_name: 'funenc_xa_station', template_name: 'good_deeds_summary'}
            })).then(function (init_data,init_department,res) {
                self.init_data = init_data;
                self.init_department = init_department;
                console.log(self.init_department );
                self.replaceElement($(res));
                var vue = new Vue({
                    el: '#good_deeds_summary',
                    data() {
                        return {
                            tableData:self.init_data,
                            department:'',
                            departments:self.init_department,
                            line:"",
                            site: self.site_data,
                            lines: '',
                            sites: self.user_site,
                            datetime: self.date_self,

                        };
                    },

                    methods: {
                        get_line: function(department_value){
                                self._rpc({
                                     model:'funenc_xa_station.good_deeds_summary',
                                     method:'get_line',
                                     kwargs: {date:department_value},
                                }).then(function(data){
                                        vue.lines = data;
                                });
                        },

                        get_site: function(department_value){
                                self._rpc({
                                     model:'funenc_xa_station.good_deeds_summary',
                                     method:'get_site',
                                     kwargs: {date:department_value},
                                }).then(function(data){
                                        vue.sites = data;
                                });
                        },

                        search_record: function(department_value){
                                self._rpc({
                                     model:'funenc_xa_station.good_deeds_summary',
                                     method:'search_record',
                                     kwargs: {department:vue.department,
                                              line:vue.line,
                                              site:vue.site,
                                              date_time:vue.datetime},
                                }).then(function(data){
                                        vue.tableData = data;
                                });
                        },

                        import_excel_belong_to_management() {
                            if (this.tableData) {
                                var url = '/funenc_xa_station/belong_to_management_summary';
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

    core.action_registry.add('good_deeds_summary', good_deeds_summary);
    return {'good_deeds_summary': good_deeds_summary};


});
