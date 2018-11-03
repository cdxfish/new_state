import odoo.exceptions as msg
from odoo import models, fields, api


class StoreHouse(models.Model):
    _name = 'funenc_xa_station2.store_house'
    _description = u'仓库管理'

    store_house_department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='仓库所属部门',
                                                default=lambda
                                                    self: self.default_store_house_department_id())
    name = fields.Char('仓库名称', required=True)

    @api.model
    def default_store_house_department_id(self):
        if self.env.user.id == 1:
            return

        return self.env.user.dingtalk_user.departments[0].id

    @api.model
    def create_store_house(self):
        context = dict(self.env.context or {})
        return {
            'name': '仓库创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station2.store_house',
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
            'res_model': 'funenc_xa_station2.store_house',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def delete(self):
        self.unlink()