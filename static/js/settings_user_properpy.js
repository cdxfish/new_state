odoo.define('settings_user_properpy', function (require) {
    'use strict';

    var Widget = require('web.Widget');
    var core = require('web.core');

    var settings_user_properpy = Widget.extend({
            init: function (parent, record, node) {
                this._super(parent, record, node);
                this.vue_data = {
                    departmentList:[],

                                defaultProps: {
                                                  children: 'children',
                                                  label: 'label'
                                                },
                };
            },
            willStart: function () {

                    var self= this;

                    return self._rpc({
                        model: 'cdtct_dingtalk.cdtct_dingtalk_users',
                        method: 'get_department_users',
                    }).then(function(data){
                        self.vue_data.departmentList = data
                    })
            },
            start: function () {
                var self = this;
                setTimeout(function () {
                    self._rpc({
                        model: 'vue_template_manager.template_manage',
                        method: 'get_template_content',
                        kwargs: {module_name: 'funenc_xa_station', template_name: 'settings_user_properpy'}
                    }).then(function (el) {
                        self.replaceElement($(el));
                        new Vue({
                            el: '#app',
                            data() {
                                return self.vue_data
                            },


                            methods: {


                                search: function () {


                                }
                            }
                        })
                    })
                })
            }
        })
    ;
    core.action_registry.add('settings_user_properpy', settings_user_properpy);
    return {settings_user_properpy: settings_user_properpy}
})
;