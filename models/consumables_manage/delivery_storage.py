import odoo.exceptions as msg
from odoo import models, fields, api


class delivery_storage(models.Model):
    _name = 'funenc_xa_station.delivery_storage'
    _description = u'耗材出库'

    department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='部门',default=lambda
        self: self.default_department_id())
    consumables_type = fields.Many2one('funenc_xa_station.consumables_type', string='耗材类型')
    consumables_count = fields.Integer(string='出库数量')
    store_house_id = fields.Many2one('funenc_xa_station.store_house',string='仓库名称')

    def default_department_id(self):
        if self.env.user.id != 1:
            return  self.env.user.dingtalk_user.departments[0].id
        else:
            return

    @api.model
    def create_delivery_storage(self):
        context = dict(self.env.context or {})
        return {
            'name': '耗材申请创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.delivery_storage',
            'context': context,
            'target': 'new',
        }

    def edit(self):
        context = dict(self.env.context or {})
        context['self_id'] = self.id
        return {
            'name': '耗材申请编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.delivery_storage',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def delete(self):
        self.unlink()

    def delivery_storage_save(self):
        pass