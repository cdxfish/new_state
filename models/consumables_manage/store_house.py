import odoo.exceptions as msg
from odoo import models, fields, api


class StoreHouse(models.Model):
    _name = 'funenc_xa_station.store_house'
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
