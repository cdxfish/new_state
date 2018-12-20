odoo.define('settings_user_property', function (require) {
    'use strict';

    var Widget = require('web.Widget');
    var core = require('web.core');

    var settings_user_property = Widget.extend({
            init: function (parent, record, node) {
                this._super(parent, record, node);
                console.log(record);
                this.vue_data = {
                                departmentList:[],
                                // 选中的人员
                                selection_user_ids:record.params.selection_user_ids,

                                defaultProps: {
                                                  children: 'children',
                                                  label: 'label'
                                                },
                                default_checked_keys:[],

                };

                if(record.params.params){
                 // 查看人员属性 因为设置人员属性和查看是一个页面所以采用传参方式
                 this.vue_data.departmentList = record.params.params.departmentList;
                 this.vue_data.default_checked_keys = record.params.params.default_checked_keys
                 this.vue_data.selection_user_ids = [record.params.params.user_id]

                }


            },

            willStart: function () {

                    var self= this;

                    return self._rpc({
                        model: 'cdtct_dingtalk.cdtct_dingtalk_users',
                        method: 'get_user_settings_departments',
                    }).then(function(data){
                        self.vue_data.departmentList = data.department_tree;
                    })
            },

            start: function () {
                var self = this;
                setTimeout(function () {
                    self._rpc({
                        model: 'vue_template_manager.template_manage',
                        method: 'get_template_content',
                        kwargs: {module_name: 'funenc_xa_station', template_name: 'settings_user_property'}
                    }).then(function (el) {
                        self.replaceElement($(el));
                        new Vue({
                            el: '#app',
                            data() {
                                return self.vue_data
                            },


                            methods: {


                                save: function () {
                                   return self._rpc({
                                        model: 'cdtct_dingtalk.cdtct_dingtalk_department',
                                        method: 'save_user_departments',
                                        kwargs: {
                                                 user_ids: self.vue_data.selection_user_ids,
                                                 department_ids: this.$refs.tree.getCheckedKeys()
                                                 }
                                    }).then(function(data){
                                       alert(data)

                                    })


                                },

                                resetChecked() {

                                    this.$refs.tree.setCheckedKeys([]);

                                 },


                            }
                        })
                    })
                })
            }
        })
    ;
    core.action_registry.add('settings_user_property', settings_user_property);
    return {settings_user_property: settings_user_property}
})
;