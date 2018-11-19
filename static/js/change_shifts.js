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
                    user:{},
                    change_shifts_ids:[
                    ],
                    take_over_from_ids:[],
                    domain:[],
                    views:[],
                    jb_form:1


                };

        },

        willStart: function () {

                    var self= this;

                    return self._rpc({
                        model: 'funenc_xa_station.production_change_shifts',
                        method: 'get_change_shifts_data'
                    }).then(function(data){
                        console.log(data.jb_form)
                          self.vue_data.user=data.user
                          self.vue_data.change_shifts_ids = data.change_shifts_ids,
                          self.vue_data.take_over_from_ids = data.take_over_from_ids,
                           self.vue_data.domain = data.domain,
                           self.vue_data.views = data.views,
                           self.vue_data.jb_form = data.jb_form

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
                        shift_shift: function(){
                            // 交班创建
//                            console.log(self.vue_data.jb_form)
                            self.do_action({
                                                name: '\u521b\u5efa',
                                                type: 'ir.actions.act_window',
                                                res_model: 'funenc_xa_station.production_change_shifts',
                                                views: [[self.vue_data.jb_form, 'form']],
                                                target: 'new'
                                            });



                        },

                        take_over_1: function(){
                            // 接班
                                                  self.do_action({
                                                            name: '\u5f85\u63a5\u73ed\u5217\u8868',
                                                            type: 'ir.actions.act_window',
                                                            res_model: 'funenc_xa_station.production_change_shifts',
                                                            views: [[self.vue_data.views, 'list']],
                                                            target: 'new',
                                                            domain:self.vue_data.domain
                                                        });


                        },

                        handleClick(tab, event) {
                            console.log(event);
                        },


                        handleEdit(index, row) {

                           self.do_action({
                                                name: '\u8be6\u60c5',
                                                type: 'ir.actions.act_window',
                                                res_model: 'funenc_xa_station.production_change_shifts',
                                                views: [[self.vue_data.jb_form, 'form']],
                                                target: 'new',
                                                flags: {'initial_mode': 'edit'},
			                                    res_id: row['id']
                                            });


                        },

                        handleDelete(index,row) {
                                    this.$confirm('是否要删除本条记录?', '提示', {
                                      confirmButtonText: '确定',
                                      cancelButtonText: '取消',
                                      type: 'warning'
                                    }).then(() => {
                                        self._rpc({
                                                    model: 'funenc_xa_station.production_change_shifts',
                                                    method: 'handle_delete',
                                                    kwargs:{id_delete:row.id}
                                                }).then(function (data) {
                                                        if(data){
                                                        self.vue_data.change_shifts_ids.splice(index, 1);
                                                        }
                                            });
                                    }).catch(() => {
                                      this.$message({
                                        type: 'info',
                                        message: '已取消删除'
                                      });
                                    });

                        },

                    handleDelete_1(index,row) {

                                this.$confirm('是否要删除本条记录?', '提示', {
                                      confirmButtonText: '确定',
                                      cancelButtonText: '取消',
                                      type: 'warning'
                                    }).then(() => {
                                        self._rpc({
                                                    model: 'funenc_xa_station.production_change_shifts',
                                                    method: 'handle_delete_1',
                                                    kwargs:{id_delete:row.id}
                                                }).then(function (data) {
                                                        if(data){
                                                        self.vue_data.take_over_from_ids.splice(index, 1);
                                                        }
                                            });
                                    }).catch(() => {
                                      this.$message({
                                        type: 'info',
                                        message: '已取消删除'
                                      });
                                    });


                        },


                    }
                })
            })
        }
    });
    core.action_registry.add('change_shifts_clint', change_shifts_clint);
    return {change_shifts_clint: change_shifts_clint}
});