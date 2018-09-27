odoo.define('funenc_xa_check', function (require) {
  "use strict";
  var core = require('web.core');
  var Widget = require('web.Widget');

  var construct_id = 12155555;

  var funenc_xa_check = Widget.extend({
    app: undefined,
    group_id: 0,
    is_update: false,
    dom_id: 'funenc_xa_check' + construct_id++,
    init: function (parent, action) {
      var self = this;
      this._super.apply(this, arguments)
      self.group_id = action.context.group_id
      self.user_data = {"result":[]};   // 部门初始化变量
      if (self.group_id) {
        self.is_update = true
      }
    },

    renderElement: function(){
      var self = this;
      var $el = $('<div id="funenc_xa_check"></div>');
      self.replaceElement($el);
    },

    start: function () {
      var self = this;

      self._rpc({
          model: 'funenc_xa_station.check_collect',
          method:'check_record_method'

        }).then(function(data){
          self.user_data=data;
        });

      this._rpc({
          model: 'vue_template_manager.template_manage',
          method: 'get_template_content',
          kwargs: {module_name: 'funenc_xa_station', template_name: 'funenc_xa_check'}
      }).then(function (res) {

           self.$el.append(res);
           setTimeout(function () {
               var vue = new Vue({
                    el: '#funenc_xa_check',
                    data() {
                       return {
                                tableData:self.user_data,
                                value6:'时间选择'

                       };
                    },

                    methods: {

                           // 点击进入方法
                            search_time: function(){

                                if (vue.value6 != '时间选择'){
                                self._rpc({
                                           model: 'funenc_xa_station.check_collect',
                                           method:'search_record_method',
                                           kwargs: {date: vue.value6}
                                                }).then(function(data){
                                                      vue.tableData =data;
                                                    });

                                                };

                              },

                        import_excel(){
                          if (this.detailData.length>0){
                            var url=this.export_url;
                            var params= {"name":this.user_name,"arr_data":this.detailData};
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
                                a.download = this.user_name+'积分列表'+(new Date()).getTime();
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

            },1000);



      });
    },


});

  core.action_registry.add('funenc_xa_check',funenc_xa_check);
  return {'funenc_xa_check':funenc_xa_check};




});
