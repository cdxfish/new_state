# -*- coding: utf-8 -*-
import odoo.exceptions as msg
from odoo import models, fields, api


class consumables_inventory(models.Model):
    _name = 'funenc_xa_station.consumables_inventory'
    _description = u'耗材库存'
    _rec_name = 'store_house'
    inventory_department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string= '库存部门')
    consumables_type = fields.Many2one('funenc_xa_station.consumables_type',string= '耗材类型')
    store_house = fields.Many2one('funenc_xa_station.store_house',string='库房位置')
    inventory_count = fields.Integer(string='库存数量')
    storage_to_consumables_ids = fields.One2many('funenc_xa_station.delivery_storage_to_consumables_inventory',
                                                 'consumables_inventory_id', string='')
    @api.model
    def create_consumables_inventory(self):
        context = dict(self.env.context or {})
        return {
            'name': '耗材出库创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.consumables_inventory',
            'context': context,
            'target': 'new',
        }

    def edit(self):
        context = dict(self.env.context or {})
        context['self_id'] = self.id
        return {
            'name': '耗材库存编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.consumables_inventory',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def delete(self):
        self.unlink()

    def consumables_inventory_save(self):
        pass