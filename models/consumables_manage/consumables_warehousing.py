import odoo.exceptions as msg
from odoo import models, fields, api
import datetime


class StoreHouse(models.Model):
    _name = 'funenc_xa_station.consumables_warehousing'
    _description = u'耗材入库'

    consumables_department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='入库部门',
                                                default=lambda self: self.default_consumables_department_id())
    consumables_type_id = fields.Many2one('funenc_xa_station.consumables_type', string='耗材名称', required=True)
    store_house_id = fields.Many2one('funenc_xa_station.store_house', string='入库名称', required=True)
    warehousing_count = fields.Integer(string='入库数量', required=True)
    warehousing_parent = fields.Selection(selection=[('purchase', '采购'), ('organize', '领用')], string='采购方式',
                                          default='organize')
    warehousing_department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='领用部门')
    outgoing_user = fields.Char(string='采购人')
    consumables_warehousing_date = fields.Date(string='入库时间')

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
