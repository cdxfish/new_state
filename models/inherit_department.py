# -*- coding: utf-8 -*-
from odoo import models, api


class inherit_department(models.Model):
    inherit = 'cdtct_dingtalk.cdtct_dingtalk_department'


    @api.model
    def get_xa_departments(self):
        return  self.sudo().search_read([],['departmentId','name','parentid'])



