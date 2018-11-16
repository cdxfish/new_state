odoo.define('funenc_xa_department_users', function (require) {
    'use strict';

    var Widget = require('web.Widget');
    var core = require('web.core');

    var funenc_xa_department_users = Widget.extend({
            init: function (parent, record, node) {
                this._super(parent, record, node);
                this.vue_data = {

                                departmentList:[],

                                defaultProps: {
                                                  children: 'children',
                                                  label: 'label'
                                                },

                                tableData: [],
                                multipleSelection: [],
                                default_checked_keys:[],
                                input:''

                };
            },
            willStart: function () {

                    var self= this;

                    return self._rpc({
                        model: 'cdtct_dingtalk.cdtct_dingtalk_users',
                        method: 'get_department_users',
                    }).then(function(data){
                        console.log(data)
                        self.vue_data.departmentList = data
                    })
            },
            start: function () {
                var self = this;
                setTimeout(function () {
                    self._rpc({
                        model: 'vue_template_manager.template_manage',
                        method: 'get_template_content',
                        kwargs: {module_name: 'funenc_xa_station', template_name: 'funenc_xa_department_users_1'}
                    }).then(function (el) {
                        console.log(el)
                        self.replaceElement($(el));
                        new Vue({
                            el: '#funenc_xa_department_users',
                            data() {
                                return self.vue_data
                            },


                            methods: {


                               search() {
                                   // 搜索
                                   if (self.vue_data.input){
                                       self._rpc({
                                                  model: 'cdtct_dingtalk.cdtct_dingtalk_users',
                                                  method:'get_user_by_name_or_no',
                                                  kwargs: {'name_or_no':self.vue_data.input}
                                                }).then(function(get_data){
                                                  self.vue_data.tableData=get_data;
                                                });


                                            }
                                   },



                               handleEdit(index, row) {

                                               self._rpc({
                                                      model: 'cdtct_dingtalk.cdtct_dingtalk_users',
                                                      method:'get_user_property_by_user_id',
                                                      kwargs: {'user_id':row['id']}
                                                    }).then(function(get_data){
//                                                      self.vue_data.default_checked_keys=get_data;
                                                      self.do_action({
                                                                name: '\u4eba\u5458\u5c5e\u6027\u8bbe\u7f6e',
                                                                type: 'ir.actions.client',
                                                                tag: 'settings_user_property',
                                                                target: 'new',
                                                                params: {
                                                                        'params':{
                                                                                  'departmentList': self.vue_data.departmentList,
                                                                                  'default_checked_keys': get_data,
                                                                                  'user_id': row['id']
                                                                        }

                                                                    }

                                                            });
                                                    });



                                  },


                                click_node: function(data){

                                   self._rpc({
                                              model: 'cdtct_dingtalk.cdtct_dingtalk_users',
                                              method:'get_users',
                                              kwargs: {'department_id':data.id}
                                            }).then(function(get_data){
                                              self.vue_data.tableData=get_data;
                                            });


                                 },

                                  handleSelectionChange(val) {
                                    var arrayObj = new Array()
                                    for(var i =0;i<val.length;i++)
                                    {
                                        arrayObj.push(val[i].id);

                                    };
                                    this.multipleSelection = arrayObj;
                                    console.log(self.vue_data.multipleSelection)


                                  },


                                  toggleSelection(rows) {
                                    if (rows) {
                                      rows.forEach(row => {
                                        this.$refs.multipleTable.toggleRowSelection(row);
                                      });
                                    } else {
                                      this.$refs.multipleTable.clearSelection();
                                    }
                                  },


                                   settings(index, row) {

                                       self.do_action({
                                                        name: '\u4eba\u5458\u5c5e\u6027\u8bbe\u7f6e',
                                                        type: 'ir.actions.client',
                                                        tag: 'settings_user_property',
                                                        target: 'new',
                                                        params: {'selection_user_ids': self.vue_data.multipleSelection}

                                                    });

                                       },



                            }
                        })
                    })
                })
            }
        })
    ;
    core.action_registry.add('funenc_xa_department_users', funenc_xa_department_users);
    return {funenc_xa_department_users: funenc_xa_department_users}
})
;
