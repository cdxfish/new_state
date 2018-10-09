import odoo.exceptions as msg
from odoo import models, fields, api


class StoreHouse(models.Model):
    _name = 'funenc_xa_station.consumables_warehousing'
    _description = u'耗材入库'

    consumables_department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='入库部门',
                                                default=lambda self: self.default_consumables_department_id())
    consumables_type_id = fields.Many2one('funenc_xa_station.consumables_type', string='耗材类型', required=True)
    store_house_id = fields.Many2one('funenc_xa_station.store_house', string='入库名称')
    warehousing_count = fields.Integer(string='入库数量')
    warehousing_parent = fields.Selection(selection=[('purchase', '采购'), ('organize', '组织')], string='采购方式',
                                          default='organize')
    warehousing_department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='采购部门')

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
        consumables_type_id = self.consumables_type_id.id
        obj = self.env['funenc_xa_station.consumables_inventory'].search(
            [('consumables_type', '=', consumables_type_id)])
        if obj:
            obj.write({'inventory_count': obj.inventory_count + self.warehousing_count})
        else:
            values = {'inventory_department_id': self.consumables_department_id.id,
                      'consumables_type': self.consumables_type_id.id,
                      'store_house': self.store_house_id.id,
                      'inventory_count': self.warehousing_count
                      }
            self.env['funenc_xa_station.consumables_inventory'].create(values)
