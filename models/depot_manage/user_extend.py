# -*- coding: utf-8 -*-

from odoo import models, fields, api


class UserExtend(models.Model):
    '''
    人员权限管理
    '''
    _inherit = 'cdtct_dingtalk.cdtct_dingtalk_users'

    enabled = fields.Boolean('是否启用', default=True)
    train_line = fields.Many2many(comodel_name="train_line.train_line")

    @api.model
    def change_groups(self):
        vals = self._context['active_ids']
        return {
            "name": "选择角色组",
            "type": "ir.actions.client",
            "tag": "change_groups_client",
            "target": "new",
            "params": vals
        }

    @api.model
    def submit_to_change(self, user_ids, role_ids):
        self.browse(user_ids).write({
            'role_group': [(6, 0, [int(i) for i in role_ids])]
        })
