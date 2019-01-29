odoo.define('selection_change_shifts_clint', function (require) {
    'use strict';

    var Widget = require('web.Widget');
    var core = require('web.core');

    var selection_change_shifts_clint = Widget.extend({
        init: function (parent, record, node) {
            this._super(parent, record, node);
            this.vue_data = {
                // position: record.params.position
                position: record.params.position
            };

        },

        start: function () {
            var self = this;
            self._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: {
                    module_name: 'funenc_xa_station',
                    template_name: 'selection_change_shifts'
                }
            }).then(function (el) {
                self.replaceElement($(el));
                new Vue({
                    el: '#app',
                    mounted(){
                    },
                    data() {
                        return self.vue_data
                    },

                    methods: {

                        station_master: function (xml_id) {
                            //值班站长
                            self._rpc({
                                model: 'funenc_xa_station.production_change_shifts',
                                method: 'get_job_form_xml_id',
                                kwargs: {
                                    xml_id: xml_id
                                }
                            }).then(function (view_xml_id) {
                                self.do_action({
                                    name: '\u521b\u5efa',
                                    type: 'ir.actions.act_window',
                                    res_model: 'funenc_xa_station.production_change_shifts',
                                    views: [[view_xml_id, 'form']],
                                    target: 'new',
                                    context: {'xml_id': view_xml_id}
                                });

                            })


                        },


                        train_working: function (xml_id) {
                            //行车值班员

                            self._rpc({
                                model: 'funenc_xa_station.production_change_shifts',
                                method: 'get_job_form_xml_id',
                                kwargs: {
                                    xml_id: xml_id
                                }
                            }).then(function (view_xml_id) {
                                self.do_action({
                                    name: '\u521b\u5efa',
                                    type: 'ir.actions.act_window',
                                    res_model: 'funenc_xa_station.production_change_shifts',
                                    views: [[view_xml_id, 'form']],
                                    target: 'new',
                                    context: {'xml_id': view_xml_id}
                                });

                            })

                        },

                        station_service: function (xml_id) {
                            // 站务员

                            self._rpc({
                                model: 'funenc_xa_station.production_change_shifts',
                                method: 'get_job_form_xml_id',
                                kwargs: {
                                    xml_id: xml_id
                                }
                            }).then(function (view_xml_id) {
                                self.do_action({
                                    name: '\u521b\u5efa',
                                    type: 'ir.actions.act_window',
                                    res_model: 'funenc_xa_station.production_change_shifts',
                                    views: [[view_xml_id, 'form']],
                                    target: 'new',
                                    context: {'xml_id': view_xml_id,'is_station_service':1}
                                });

                            })

                        },

                        ticket_booth: function (xml_id) {
                            //票亭岗

                            self._rpc({
                                model: 'funenc_xa_station.production_change_shifts',
                                method: 'get_job_form_xml_id',
                                kwargs: {
                                    xml_id: xml_id
                                }
                            }).then(function (view_xml_id) {
                                self.do_action({
                                    name: '\u521b\u5efa',
                                    type: 'ir.actions.act_window',
                                    res_model: 'funenc_xa_station.production_change_shifts',
                                    views: [[view_xml_id, 'form']],
                                    target: 'new',
                                    context: {'xml_id': view_xml_id}
                                });

                            })

                        },

                        passenger_transport: function (xml_id) {
                            //客运值班员

                            self._rpc({
                                model: 'funenc_xa_station.production_change_shifts',
                                method: 'get_job_form_xml_id',
                                kwargs: {
                                    xml_id: xml_id
                                }
                            }).then(function (view_xml_id) {
                                self.do_action({
                                    name: '\u521b\u5efa',
                                    type: 'ir.actions.act_window',
                                    res_model: 'funenc_xa_station.production_change_shifts',
                                    views: [[view_xml_id, 'form']],
                                    target: 'new',
                                    context: {'xml_id': view_xml_id}
                                });

                            })

                        },

                        return_button: function () {
                            //返回

                            self.do_action({
                                'name': '交接班选择',
                                'type': 'ir.actions.client',
                                'tag': 'change_shifts_clint',
                                'target': 'current'
                            });

                        }


                    }
                })
            })
        }
    });

    core.action_registry.add('selection_change_shifts_clint', selection_change_shifts_clint);

    return {selection_change_shifts_clint: selection_change_shifts_clint}

});