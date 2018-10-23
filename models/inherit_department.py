# -*- coding: utf-8 -*-
from odoo import models, api


class inherit_department(models.Model):
    inherit = 'cdtct_dingtalk.cdtct_dingtalk_department'

    @api.model
    def get_xa_departments(self):
        return self.sudo().search_read([], ['departmentId', 'name', 'parentid'])

    @api.model
    def get_users_by_department_id(self, departmentid):
        users = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].sudo().search_read([('departments', '=', departmentid)]
                                                                                   ,['id','jobnumber','name','departments'])
        for user in users:
            user['departmentId'] = user.get('departments')
        return users
