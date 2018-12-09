odoo.define('staion_equipment_summary', function (require) {
    "use strict";
    var core = require('web.core');
    var Widget = require('web.Widget');


    var staion_equipment_summary = Widget.extend({
        init: function (parent, action) {
            var self = this;
            this._super.apply(this, arguments);
            self.date_self = new Date();
        },
        start: function () {
            var self = this;

            $.when(
                    self._rpc({
                        model: 'funenc_xa_station.good_deeds_summary',
                        method: 'get_department',
                    }),
                    self._rpc({
                        model: 'funenc_xa_station.station_equipment_summary',
                        method: 'get_equipment_name',
                    }),
                    self._rpc({
                        model: 'funenc_xa_station.station_equipment_summary',
                        method: 'get_name_all',
                    }),

            this._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: {module_name: 'funenc_xa_station', template_name: 'staion_equipment_summary'}
            })).then(function (init_department,all_record,all_name,res) {
                self.init_department = init_department;
                self.all_record = all_record;
                self.all_name = all_name;
                self.replaceElement($(res));
                var vue = new Vue({
                    el: '#staion_equipment_summary',
                    data() {
                        return {
                            tableData: self.all_record,
                            department:'',
                            departments:self.init_department,
                            line:"",
                            site: '',
                            lines: '',
                            sites: '',
                            datetime: '',
                            equipment_name:'',
                            equipment_names:self.all_name,

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
                                if (department_value){

                                self._rpc({
                                     model:'funenc_xa_station.good_deeds_summary',
                                     method:'get_site',
                                     kwargs: {date:department_value},
                                }).then(function(data){
                                        vue.sites = data;
                                });
                                };
                        },

                        search: function(department_value){
                                self._rpc({
                                     model:'funenc_xa_station.station_summary',
                                     method:'clint_search'
                                     kwargs: {department:vue.department,
                                              line:vue.line,
                                              site:vue.site,
                                              equipment_name:vue.equipment_name},
                                }).then(function(data){
                                        vue.sites = data;
                                });
                        },

                        import_excel_belong_to_management() {
                            if (this.tableData) {
                                var url = '/funenc_xa_station/station_equipment_summary';
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
                                        a.download = '车站设备汇总' + (new Date()).getTime();
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

    core.action_registry.add('staion_equipment_summary', staion_equipment_summary);
    return {'staion_equipment_summary': staion_equipment_summary};


});
