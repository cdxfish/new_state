# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api,models,fields

class BreakTypeIncrease(models.Model):
    _name = 'funenc_xa_staion.break_type_increase'

    _rec_name = 'break_type'
    break_type = fields.Char(string='故障类型')
    note = fields.Char(string='备注')


    @api.model
    def get_break_type(self):

        return self.search_read([],['id','break_type'])
