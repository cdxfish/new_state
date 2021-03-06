# -*- coding: utf-8 -*-
from odoo import models, fields, api

from ..get_domain import get_site_ids

class consumables_inventory(models.Model):
    _name = 'funenc_xa_station.consumables_inventory'
    _description = u'耗材库存'
    _rec_name = 'store_house'
    _order = 'id desc'

    inventory_department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='库存部门')
    consumables_type = fields.Many2one('funenc_xa_station.consumables_type', string='耗材名称')
    store_house = fields.Many2one('funenc_xa_station.store_house', string='库房位置')
    inventory_count = fields.Integer(string='库存数量')
    storage_to_consumables_ids = fields.One2many('funenc_xa_station.delivery_storage_to_consumables_inventory',
                                                 'consumables_inventory_id', string='')
    inventory_department_id_son = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='库存部门')
    outgoing_way = fields.Selection([('person', '个人'), ('organization', '组织')], string='出库对象')
    outgoing_user = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='个人姓名')
    inventory_export = fields.Integer(string='库存数量')
    department_name = fields.Char(string='部门名称')


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

    @api.multi
    def rk(self):
        context = {}
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_consumables_warehousing_form').id
        return {
            'name': '入库',
            "type": "ir.actions.act_window",
            "res_model": "funenc_xa_station.consumables_warehousing",
            "views": [[view_form, "form"]],
            'target': 'new',
            'context': context
        }

    @api.multi
    def sq(self):
        context = {}
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_consumables_apply_form').id
        return {
            'name': '申请',
            "type": "ir.actions.act_window",
            "res_model": "funenc_xa_station.consumables_apply",
            "views": [[view_form, "form"]],
            'target': 'new',
            'context': context
        }
    @get_site_ids
    @api.multi
    def crkjl(self,site_ids):
        view_tree = self.env.ref('funenc_xa_station.funenc_xa_station_consumables_warehousing_list').id
        return {
            'name': '耗材入库',
            'type': 'ir.actions.act_window',
            'domain':[('consumables_department_id','=',site_ids)],
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.consumables_warehousing',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                                      [
                                          {
                                              'title': '耗材入库',
                                              'action' : 'funenc_xa_station.funenc_xa_station_consumables_warehousing_server',
                                              },
                                          {
                                              'title': '耗材出库',
                                              'action2':  'funenc_xa_station.xa_station_consumables_delivery_storage',
                                              
                                              },
                                      ]
                                  }''',
            'context': self.env.context,
        }

    # 出库编辑按钮
    def out(self):
        context = dict(self.env.context or {})
        context['apply_id'] = self.id
        context['department_id'] = self.inventory_department_id.id
        context['consumables_type'] = self.consumables_type.id
        context['store_house_id'] = self.store_house.id
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_delivery_storage_form').id
        return {
            'name': '出库',
            "type": "ir.actions.act_window",
            "res_model": "funenc_xa_station.delivery_storage",
            "views": [[view_form, "form"]],
            'target': 'new',
            'context': context,
        }

    @api.model
    def init_data(self):
        if self.env.user.id == 1:
            domain = []
        else:
            ding_user = self.env.user.dingtalk_user
            ids = ding_user.user_property_departments.ids
            domain = [('inventory_department_id','=',ids)]

        context = dict(self.env.context or {})
        view_tree = self.env.ref('funenc_xa_station.funenc_xa_station_consumables_inventory_list').id
        return {
            'name': '出库',
            "type": "ir.actions.act_window",
            "res_model": "funenc_xa_station.consumables_inventory",
            "views": [[view_tree, "tree"]],
            'target': 'current',
            'context': context,
            'domain':domain
        }
