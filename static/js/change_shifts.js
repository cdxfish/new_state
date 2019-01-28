/**
 * Created by artorias on 2018/10/28.
 */
odoo.define('change_shifts_clint', function (require) {
    'use strict';

    var Widget = require('web.Widget');
    var core = require('web.core');

    var change_shifts_clint = Widget.extend({
        init: function (parent, record, node) {
            this._super(parent, record, node);
            this.vue_data = {
                activeName: 'first',
                user: {},
                change_shifts_ids: [],
                take_over_from_ids: [],
                domain: [],
                views: [],
                position: '',
                job_form:''

            };

        },

        willStart: function () {

            var self = this;

            return self._rpc({
                model: 'funenc_xa_station.production_change_shifts',
                method: 'get_change_shifts_data'
            }).then(function (data) {
                console.log(data);
                self.vue_data.user = data.user,
                    self.vue_data.change_shifts_ids = data.change_shifts_ids,
                    self.vue_data.take_over_from_ids = data.take_over_from_ids,
                    self.vue_data.domain = data.domain,
                    self.vue_data.views = data.views,
                    self.vue_data.position = data.position,
                    self.vue_data.job_form = data.job_form


            })
        },
        start: function () {
            var self = this;
            self._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: {
                    module_name: 'funenc_xa_station',
                    template_name: 'change_shifts'
                }
            }).then(function (el) {
                self.replaceElement($(el));
                new Vue({
                    el: '#app',
                    data() {
                        return self.vue_data
                    },

                    methods: {
                        shift_shift: function () {
                            // 交接班选择
                            var position = self.vue_data.position;
                            alert(self.vue_data.job_form);
                            if (position == 'passenger_transport') {
                                alert(1);
                                self.do_action({
                                    name: '\u521b\u5efa',
                                    type: 'ir.actions.act_window',
                                    res_model: 'funenc_xa_station.production_change_shifts',
                                    views: [[self.vue_data.job_form, 'form']],
                                    target: 'new'
                                });

                            } else if (position == 'ticket_booth') {
                                 alert(2);
                                self.do_action({
                                    name: '\u521b\u5efa',
                                    type: 'ir.actions.act_window',
                                    res_model: 'funenc_xa_station.production_change_shifts',
                                    views: [[self.vue_data.job_form, 'form']],
                                    target: 'new'
                                });

                            } else {
                                 alert(3);
                                self.do_action({
                                    'name': '交接班选择',
                                    'type': 'ir.actions.client',
                                    'tag': 'selection_change_shifts_clint',
                                    'target': 'current',
                                    'params': {'position': self.vue_data.position}

                                });

                            }


                        },

                        take_over_1: function () {
                            // 接班
                            self.do_action({
                                name: '\u5f85\u63a5\u73ed\u5217\u8868',
                                type: 'ir.actions.act_window',
                                res_model: 'funenc_xa_station.production_change_shifts',
                                views: [[self.vue_data.views, 'list']],
                                target: 'new',
                                domain: self.vue_data.domain
                            });


                        },

                        handleClick(tab, event) {
                        },


                        handleEdit(index, row) {
                            self.do_action({
                                name: '\u8be6\u60c5',
                                type: 'ir.actions.act_window',
                                res_model: 'funenc_xa_station.production_change_shifts',
                                views: [[row.xml_id, 'form']],
                                target: 'new',
                                flags: {'initial_mode': 'edit'},
                                res_id: row['id']
                            });

                        },

                        handleDelete(index, row) {
                            var this_vue = this;
                            this.$confirm('是否要删除本条记录?', '提示', {
                                confirmButtonText: '确定',
                                cancelButtonText: '取消',
                                type: 'warning'
                            }).then(() = > {
                                self._rpc({
                                    model: 'funenc_xa_station.production_change_shifts',
                                    method: 'handle_delete',
                                    kwargs: {id_delete: row.id}
                                }).then(function (data) {
                                    if (data) {
                                        self.vue_data.change_shifts_ids.splice(index, 1);
                                    } else {
                                        this_vue.$message({
                                            message: '只能删除草稿状态下的交接班',
                                            type: 'warning'
                                        });
                                    }


                                });
                        }).
                            catch(() = > {
                                this.$message({
                                    type: 'info',
                                    message: '已取消删除'
                                });
                        })
                            ;

                        },


                    }
                })
            })
        }
    });
    core.action_registry.add('change_shifts_clint', change_shifts_clint);
    return {change_shifts_clint: change_shifts_clint}
});