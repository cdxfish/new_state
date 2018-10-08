import odoo.exceptions as msg
from odoo import models, fields, api


class StoreHouse(models.Model):
    _name = 'funenc_xa_station.consumables_apply'
    _description = u'耗材申请'

    to_department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='目标部门', default=lambda
        self: self.default_to_department_id())
    to_parent_department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='目标父部门')
    department_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='申请部门',default=lambda
        self: self.default_department_id())
    consumables_type = fields.Many2one('funenc_xa_station.consumables_type', string='耗材类型')
    consumables_count = fields.Integer(string='申请数量')

    @api.model
    def create_consumables_apply(self):
        context = dict(self.env.context or {})
        return {
            'name': '耗材申请创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.consumables_apply',
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
            'res_model': 'funenc_xa_station.consumables_apply',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def delete(self):
        self.unlink()


    def default_to_department_id(self):
        if self.env.user.id != 1:
            department_id = self.env.user.dingtalk_user.departments[0]
            parent_department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([('departmentId','=',department_id.parentid)])
            return  parent_department.id or None
        else:
            return

    def default_department_id(self):
        if self.env.user.id != 1:
            return  self.env.user.dingtalk_user.departments[0].id
        else:
            return

    def consumables_apply_save(self):
        pass


