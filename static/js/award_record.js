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
      self.user_data = {"result":[]};   // 部门初始化变量
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
                                datetime:'时间选择'

                       };
                    },

                    methods: {

                           // 单击节点
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







                    },

                    });

            },1000);



      });
    },


});

  core.action_registry.add('funenc_xa_award',funenc_xa_award);
  return {'funenc_xa_award':funenc_xa_award};




});
