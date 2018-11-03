# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ArrangeClassManage(models.Model):
    _name = 'funenc_xa_station2.arrange_class_manage'
    _description = u'排班规则管理'
    _inherit = 'fuenc_station.station_base'

    arrange_class_type = fields.Many2many('funenc_xa_station2.arrange_order','arrange_class_manage_arrange_order_1_ref',
                                          'arrange_class_manage_id', 'arrange_order_id',string='排班类型', required=True)
    arrange_class_obj = fields.Many2one('funenc_xa_station2.class_group', string='对象', required=True)  # 班组对象
    remarks= fields.Text(string='备注')


    @api.model
    def create_arrange_class_manage(self):
        return {
            'name': '新增排班规则',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station2.arrange_class_manage',
            'context': self.env.context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def arrange_class_manage_edit(self):
        return {
            'name': '排班规则详情编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station2.arrange_class_manage',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def arrange_class_manage_delete(self):
        # 还差在使用不能删除的判断
        self.unlink()

