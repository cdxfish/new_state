# -*- coding: utf-8 -*-
import odoo.exceptions as msg

from odoo import models, fields, api

class position_settiings(models.Model):
    _inherit = 'cdtct_dingtalk.cdtct_dingtalk_users'
    _description = '人员职位设置'

    name = fields.Char(string='职位名称')

