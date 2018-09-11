odoo.define('funenc_xa_department_users', function (require) {
  "use strict";
  var core = require('web.core');
  var Widget = require('web.Widget');

  var construct_id = 9090;

  var funenc_xa_department_users = Widget.extend({
    app: undefined,
    group_id: 0,
    is_update: false,
    dom_id: 'key_statistic' + construct_id++,
    init: function (parent, action) {
      var self = this;
      this._super.apply(this, arguments)
      self.group_id = action.context.group_id
      self.department_data = {"result":[]};   // 部门初始化变量
//      self.department_user_data = {"result":[]}; // 部门人员初始化
      if (self.group_id) {
        self.is_update = true
      }
    },

    renderElement: function(){
      var self = this;
      var $el = $('<div id="funenc_xa_department_users"></div>');
      self.replaceElement($el);
    },

    start: function () {
      var self = this;

      self._rpc({
          model: 'cdtct_dingtalk.cdtct_dingtalk_users',
          method:'get_department_users'

        }).then(function(data){
          self.department_data=data;
        });


      this._rpc({
          model: 'vue_template_manager.template_manage',
          method: 'get_template_content',
          kwargs: {module_name: 'funenc_xa_station', template_name: 'funenc_xa_department_users'}
      }).then(function (res) {

           self.$el.append(res);
           setTimeout(function () {
               var vue = new Vue({
                    el: '#funenc_xa_department_users',
                    data() {
                       return {
                                departmentList:self.department_data[0],

                                defaultProps: {
                                                  children: 'children',
                                                  label: 'label'
                                                },

                                tableData: self.department_data[1],


                       };
                    },

                    methods: {

                       // 单击节点
                       click_node: function(data){

                               self._rpc({
                                          model: 'cdtct_dingtalk.cdtct_dingtalk_users',
                                          method:'get_users',
                                          kwargs: {'department_id':data.id}
                                        }).then(function(get_data){
                                          vue.tableData=get_data;
                                        });


                       },



                    }

                    });

            },1000);



      });
    }


});

  core.action_registry.add('funenc_xa_department_users',funenc_xa_department_users);
  return {'funenc_xa_department_users':funenc_xa_department_users};




});
