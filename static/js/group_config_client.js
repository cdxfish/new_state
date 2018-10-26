/**
 * Created by artorias on 2018/10/19.
 */
odoo.define('group_config_client', function (require) {
    'use strict';

    var Widget = require('web.Widget');
    var core = require('web.core');

    var group_config_client = Widget.extend({
        template: '',
        init: function (parent, record, node) {
            this._super(parent, record, node);
            this.group_id = record.params.type === 'add' ? null : record.context.active_id;
            this.vue_data = {
                open_type: record.params.type,
                normalCats: [],
                group_name: '',
                group_tree_data: [],
                defaultProps: {
                    children: 'children',
                    label: 'name'
                }
            }
        },
        start: function () {
            var self = this;
            self._rpc({
                model: 'res.groups',
                method: 'get_group_data',
                kwargs: {group_id: self.group_id}
            }).then(function (rst) {
                self.replaceElement($(rst.template));
                self.vue_data.normalCats = rst.cats;
                self.vue_data.group_tree_data = rst.cats;
                new Vue({
                    el: '#app',
                    data() {
                        return self.vue_data
                    },
                    methods: {
                        save_group: function () {
                            if (this.open_type === 'add' && this.group_name === '') {
                                this.$notify({
                                    title: '警告',
                                    message: '名称不能为空',
                                    type: 'warning'
                                });
                                return
                            }
                            self._rpc({
                                model: 'res.groups',
                                method: 'add_or_write_custom_group',
                                args: [this.open_type, self.group_id, this.group_name, this.normalCats],
                            }).then(function () {
                                self.do_action({
                                    type: 'ir.actions.act_window_close'
                                })
                            })
                        },
                        handleCheckAllChange: function (cat) {
                            if (cat.checkAll) {
                                cat.checkedGroups = _.pluck(cat.groups, 'id');
                            } else {
                                cat.checkedGroups = []
                            }
                            cat.isIndeterminate = false
                        },
                        handleCheckedCitiesChange: function (cat, checkedGroups, groups) {
                            var checkedCount = checkedGroups.length;
                            cat.checkAll = checkedCount === groups.length;
                            cat.isIndeterminate = checkedCount > 0 && checkedCount < cat.groups.length;
                        },
                        handleNodeClick(data) {
                            console.log(data);
                        }
                    },
                })
            })
        }
    });
    core.action_registry.add('group_config_client', group_config_client);
    return {group_config_client: group_config_client}
});