odoo.define('funenc_xa_motorized_users', function (require) {
  "use strict";
  var core = require('web.core');
  var Widget = require('web.Widget');

  var construct_id = 12123;

  var funenc_xa_motorized_users = Widget.extend({
    app: undefined,
    group_id: 0,
    is_update: false,
    dom_id: 'motorized_user' + construct_id++,
    init: function (parent, action) {
      var self = this;
      this._super.apply(this, arguments)
      self.group_id = action.context.group_id
      self.user_data = {"result":[]};   // 部门初始化变量
//      self.department_user_data = {"result":[]}; // 部门人员初始化
      if (self.group_id) {
        self.is_update = true
      }
    },

    renderElement: function(){
      var self = this;
      var $el = $('<div id="funenc_xa_motorized_users"></div>');
      self.replaceElement($el);
    },

    start: function () {
      var self = this;

      self._rpc({
          model: 'cdtct_dingtalk.cdtct_dingtalk_users',
          method:'get_motorized_users'

        }).then(function(data){
          self.user_data=data;
        });


      this._rpc({
          model: 'vue_template_manager.template_manage',
          method: 'get_template_content',
          kwargs: {module_name: 'funenc_xa_station', template_name: 'funenc_xa_motorized_users'}
      }).then(function (res) {

           self.$el.append(res);
           setTimeout(function () {
               var vue = new Vue({
                    el: '#funenc_xa_motorized_users',
                    data() {
                       return {

                                tableData: self.user_data,

                       };
                    },

                    methods: {

                           // 单击节点
                            handleEdit(index, row) {
                            alert(row['user_property'])

                               self.do_action({
                                                name: '\u673a\u52a8\u4eba\u5458\u7ba1\u7406',
                                                type: 'ir.actions.act_window',
                                                res_model: 'cdtct_dingtalk.cdtct_dingtalk_users',
                                                views: [[false, 'form']],
                                                target: 'new',
                                                flags: {'initial_mode': 'edit'},
			                                    res_id: row['id']
                                            });


//                                alert(row['id'])
//                                    self._rpc({
//                                          model: 'cdtct_dingtalk.cdtct_dingtalk_users',
//                                          method:'get_users',
//                                          kwargs: {'department_id':data.id}
//                                        }).then(function(get_data){
//                                          vue.tableData=get_data;
//                                        });
                              },







                    },

                    });

            },1000);



      });
    },


});

  core.action_registry.add('funenc_xa_motorized_users',funenc_xa_motorized_users);
  return {'funenc_xa_motorized_users':funenc_xa_motorized_users};




});
