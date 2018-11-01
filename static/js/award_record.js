odoo.define('funenc_xa_award', function (require) {
  "use strict";
  var core = require('web.core');
  var Widget = require('web.Widget');

  var construct_id = 123451;

  var funenc_xa_award = Widget.extend({
    app: undefined,
    group_id: 0,
    is_update: false,
    dom_id: 'funenc_xa_award' + construct_id++,
    init: function (parent, action) {
      var self = this;
      this._super.apply(this, arguments)
      self.group_id = action.context.group_id

       self._rpc({
            model:'funenc_xa_station.award_collect',
            method:'get_group_2'
      }).then(function(data){
      console.log(data);
        if(data ){
            self.data_2 = true;
        }else{
            self.data_2 = false;
        };
      });

    self._rpc({
            model:'funenc_xa_station.award_collect',
            method:'get_group_1'
      }).then(function(data){
      console.log(data);
        if(data ){
            self.data_1 = true;
        }else{
            self.data_1 = false;
        };
      });

    self._rpc({
            model:'funenc_xa_station.award_collect',
            method:'get_group_3'
      }).then(function(data){
      console.log(data);
        if(data ){
            self.data_3 = true;
        }else{
            self.data_3 = false;
        };
      });

      self._rpc({
            model:'funenc_xa_station.award_collect',
            method:'get_group_4'
      }).then(function(data){
      console.log(data);
        if(data ){
            self.data_4 = true;
        }else{
            self.data_4 = false;
        };
      });
      self.user_data = [];   // 部门初始化变量
      if (self.group_id) {
        self.is_update = true
      }
    },

    renderElement: function(){
      var self = this;
      var $el = $('<div id="funenc_xa_award"></div>');
      self.replaceElement($el);
    },

    start: function () {
      var self = this;

      self._rpc({
          model: 'funenc_xa_station.award_collect',
          method:'award_record_method'

        }).then(function(data){
          self.user_data=data;
        });

      this._rpc({
          model: 'vue_template_manager.template_manage',
          method: 'get_template_content',
          kwargs: {module_name: 'funenc_xa_station', template_name: 'funenc_xa_award'}
      }).then(function (res) {
           self.$el.append(res);
           setTimeout(function () {
               var vue = new Vue({
                    el: '#funenc_xa_award',
                    data() {
                       return {
                                tableData:self.user_data,
                                datetime:'时间选择',
                                activeIndex:'1',
                                tabValue:'',
                                show_1:self.data_1,
                                show_2:self.data_2,
                                show_3:self.data_3,
                                show_4:self.data_4,

                       };
                    },

                    methods: {

                            search_time: function(){

                                if (vue.datetime != '时间选择'){
                                self._rpc({
                                           model: 'funenc_xa_station.award_collect',
                                           method:'search_award_method',
                                           kwargs: {date: vue.datetime}
                                                }).then(function(data){
                                                      vue.tableData =data;
                                                    });

                                                };

                              },

//                          tab页面的跳转功能
                           handleSelect: function(){
                                    var that =this;
                                    if(that.tabValue==1){
                                        self._rpc({
                                            model:'funenc_xa_station.check_record',
                                            method:'get_action',
                                         }).then(function(data){
//                                            console.log(data);
                                            self.do_action(data);
                                            });
                                     }else if(that.tabValue==2){
                                                    self._rpc({
                                                    model:'funenc_xa_station.check_collect',
                                                    method:'get_action',
                                                 }).then(function(data){
//                                                    console.log(data);
                                                    self.do_action(data);
                                                    });
                                            }
                                      else if(that.tabValue==3){
                                         self._rpc({
                                                model:'funenc_xa_station.award_record',
                                                method:'get_action',
                                             }).then(function(data){
                                                self.do_action(data);
                                                });
                                     }else if(that.tabValue==4){
                                                 self._rpc({
                                                    model:'funenc_xa_station.check_collect',
                                                    method:'get_action',
                                                 }).then(function(data){
//                                                    console.log(data);
                                                    self.do_action(data);
                                                    });
                                     };

                               },

                       import_award(){
                          if (this.tableData){
                            var url='/fuenc_xa_station/award_collect_download';
                            var params= {"exl_data":this.tableData};
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
                                a.download = '奖励汇总'+(new Date()).getTime();
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

  core.action_registry.add('funenc_xa_award',funenc_xa_award);
  return {'funenc_xa_award':funenc_xa_award};




});
