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
                        kwargs: {module_name: 'funenc_xa_station', template_name: 'funenc_xa_department_users'}
                    }).then(function (el) {
                        self.replaceElement($(el));
                        new Vue({
                            el: '#funenc_xa_department_users',
                            data() {
                                return self.vue_data
                            },


                            methods: {


                                click_node: function(data){

                                   self._rpc({
                                              model: 'cdtct_dingtalk.cdtct_dingtalk_users',
                                              method:'get_users',
                                              kwargs: {'department_id':data.id}
                                            }).then(function(get_data){
                                              self.vue_data.tableData=get_data;
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
