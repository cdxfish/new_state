import odoo.exceptions as msg
from odoo import models, fields, api
import datetime
from ..get_domain import get_site_ids
import json

class StoreHouse(models.Model):
    _name = 'funenc_xa_station.consumables_warehousing'
    _description = u'耗材入库'
    _order = 'id desc'
    _rec_name = 'consumables_department_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    consumables_department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='入库部门', track_visibility='onchange',
                                                # default=lambda self: self.default_consumables_department_id()
                                                )
    consumables_type_id = fields.Many2one('funenc_xa_station.consumables_type', string='耗材名称', required=True, track_visibility='onchange')
    store_house_id = fields.Many2one('funenc_xa_station.store_house', string='入库名称', required=True, track_visibility='onchange')
    warehousing_count = fields.Integer(string='入库数量', required=True, track_visibility='onchange')
    warehousing_parent = fields.Selection(selection=[('purchase', '采购'), ('organize', '领用')], string='采购方式',
                                          default='organize', track_visibility='onchange')
    warehousing_department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='领用人', track_visibility='onchange')
    outgoing_user = fields.Char(string='采购部门', track_visibility='onchange')
    consumables_warehousing_date = fields.Date(string='入库时间', track_visibility='onchange')

    product_departments_domain = fields.Char(
        compute="_compute_product_departments_domain",
        readonly=True,
        store=False,
    )

    @api.multi
    @api.depends('consumables_department_id')
    def _compute_product_departments_domain(self):
        if self.env.user.id == 1:
            domain = []
        else:
            departments_ids = self.env.user.dingtalk_user.user_property_departments.ids
            domain = [('id', 'in', departments_ids)]

        for rec in self:
            rec.product_departments_domain = json.dumps(
                domain
            )

    @api.model
    def create_consumables_warehousing(self):
        context = dict(self.env.context or {})
        return {

            'name': '耗材入库创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.consumables_warehousing',
            'context': context,
            'target': 'new',
        }

    def edit(self):
        context = dict(self.env.context or {})
        return {
            'name': '编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.consumables_warehousing',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def delete(self):
        self.unlink()

    @api.onchange('warehousing_parent')
    def filter_warehousing_site_id(self):
        if self.warehousing_parent == 'organize':
            self.warehousing_department_id = None

    @api.model
    def default_consumables_department_id(self):
        if self.env.user.id == 1:
            return

        return self.env.user.dingtalk_user.departments[0].id

    def consumables_warehousing_save(self):
        self.consumables_warehousing_date = datetime.datetime.now()
        obj = self.env['funenc_xa_station.consumables_inventory'].search(
            [('consumables_type', '=', self.consumables_type_id.id),
             ('store_house', '=', self.store_house_id.id),
             ('inventory_department_id','=',self.consumables_department_id.id)])
        if obj:
            obj.write({'inventory_count': obj.inventory_count + self.warehousing_count})
        else:
            values = {'inventory_department_id': self.consumables_department_id.id,
                      'consumables_type': self.consumables_type_id.id,
                      'store_house': self.store_house_id.id,
                      'inventory_count': self.warehousing_count
                      }

            self.env['funenc_xa_station.consumables_inventory'].create(values)
    @get_site_ids
    @api.multi
    def get_day_plan_publish_action(self,site_ids):
        view_tree = self.env.ref('funenc_xa_station.funenc_xa_station_consumables_warehousing_list').id
        return {
            'name': '耗材入库',
            'type': 'ir.actions.act_window',
            'domain': [('consumables_department_id','in',site_ids)],
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
