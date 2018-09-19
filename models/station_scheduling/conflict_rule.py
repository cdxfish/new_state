# -*- coding: utf-8 -*-

import odoo.exceptions as msg
from odoo import models, fields, api


class ConflictRule(models.Model):
    _name = 'funenc_xa_station.conflict_rule'
    _description = '冲突规则'
    _order = 'conflict_rule_index asc'
    _inherit = 'fuenc_station.station_base'

    conflict_rule_index = fields.Integer(string='序号', default =1)
    conflict_rule_content = fields.Char(string='内容')
    conflict_rule = fields.Char(string='条件')
    conflict_rule_state = fields.Selection(selection=[('enable','启用'), ('discontinuation', '停用')])

    is_certificate = fields.Integer(string='证书', default =1)  #用来判断该记录是否是证书具备
    station_certificate_ids = fields.One2many('station.certificate', 'conflict_rule_id', string='')

