# -*- coding: utf-8 -*-

from odoo import models, fields, api

from ..get_domain import get_domain


class ArrangeClassManage(models.Model):
    _name = 'funenc_xa_station.arrange_class_manage'
    _description = u'排班规则管理'
    _inherit = 'fuenc_station.station_base'

    name = fields.Char(string='名称', compute='_compute_name')

    obj_selection = fields.Selection(selection=[('arrange_class', '班组'), ('motorized', '机动人员')],
                                     default="arrange_class")  # 班组对象
    remarks = fields.Text(string='备注')

    order_to_arrange_ids = fields.One2many('arrange_order_to_arrange_class_manage', 'arrange_class_manage_id',
                                           string='排班类型', required=True)

    @get_domain
    @api.model
    def init_data(self, domain):
        context = {}
        view_tree = self.env.ref('funenc_xa_station.funenc_xa_station_arrange_class_manage_list').id
        return {
            'name': '排班规则管理',
            "type": "ir.actions.act_window",
            "res_model": "funenc_xa_station.arrange_class_manage",
            "views": [[view_tree, "tree"]],
            "domain": domain,
            'target': 'current',
            'context': context,
        }

    def _compute_name(self):
        for this in self:
            name = ''
            for i, order_to_arrange_id in enumerate(this.order_to_arrange_ids):
                if i == 0:
                    name = name + order_to_arrange_id.arrange_order_id.name if order_to_arrange_id else ''

                else:
                    name = name + ',' + order_to_arrange_id.arrange_order_id.name if order_to_arrange_id else ''
            this.name = name

    @api.model
    def create_arrange_class_manage(self):
        return {
            'name': '新增排班规则',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.arrange_class_manage',
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
            'res_model': 'funenc_xa_station.arrange_class_manage',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def arrange_class_manage_delete(self):
        # 还差在使用不能删除的判断
        self.unlink()


class ArrangeOrderToArrangeClassManage(models.Model):
    _name = 'arrange_order_to_arrange_class_manage'
    _description = '班次和排班规则中间表'

    arrange_class_manage_id = fields.Many2one('funenc_xa_station.arrange_class_manage', string='排班规则')
    arrange_order_id = fields.Many2one('funenc_xa_station.arrange_order', string='排班班次')
