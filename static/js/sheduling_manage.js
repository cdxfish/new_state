odoo.define('funenc_xa_station_sheduling_manage', function (require) {
  "use strict";
  var core = require('web.core');
  var Widget = require('web.Widget');

  var construct_id = 12345;

  var funenc_xa_station_sheduling_manage = Widget.extend({
    app: undefined,
    group_id: 0,
    is_update: false,
    dom_id: 'funenc_xa_station_sheduling_manage' + construct_id++,
    init: function (parent, record, action) {
      var self = this;
      self.res_id = record.res_id;
      this._super.apply(this, arguments);
//      self.group_id = action.context.group_id;
      self.sheduling_data = {"result":[]};   // 声明钥匙统计变量
//      if (self.group_id) {
//        self.is_update = true
//      }
    },

    renderElement: function(){
      var self = this;
      var $el = $('<div id="funenc_xa_station_sheduling_manage"></div>');
      self.replaceElement($el);
    },

    start: function () {
      var self = this;
      if (self.res_id == null){
         return
      }
      self._rpc({
          model: 'funenc_xa_station.sheduling_manage',
          method:'sheduling_start',
          kwargs:{res_id: self.res_id}

        }).then(function(data){
          self.sheduling_data=data;
        });




      this._rpc({
          model: 'vue_template_manager.template_manage',
          method: 'get_template_content',
          kwargs: {module_name: 'funenc_xa_station', template_name: 'sheduling_manage'}
      }).then(function (res) {

           self.$el.append(res);
           setTimeout(function () {
                   new Vue({
                    el: '#funenc_xa_station_sheduling_manage',
                    data() {
                       return {

                             group_data: self.sheduling_data[3],
                             group_cols: self.sheduling_data[1],
                             motorized_cols: self.sheduling_data[2],
                             motorizedData: self.sheduling_data[4],
                             show_position1: self.sheduling_data[0][0],
                             show_sheduling_time: self.sheduling_data[0][1],
                             show_arrange_order_name1: self.sheduling_data[0][2],
                             current_rule: self.sheduling_data[0][3],
                             groupCountData:[]


                       };
                    },

                    methods: {

                       // 钥匙创建
                       create_key: function(){

                            self.do_action({
                                                name: '\u94a5\u5319\u65b0\u5efa',
                                                type: 'ir.actions.act_window',
                                                res_model: 'funenc.xa.station.key.detail',
                                                views: [[false, 'form']],
                                                target: 'new'
                                            });


                       },





                    }

                    });

            },1000);



      });
    }


});

  core.action_registry.add('funenc_xa_station_sheduling_manage',funenc_xa_station_sheduling_manage);

  return {'funenc_xa_station_sheduling_manage':funenc_xa_station_sheduling_manage};




});
