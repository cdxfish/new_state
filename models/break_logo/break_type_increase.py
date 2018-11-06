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


    def onchange_record(self):
        view_form = self.env.ref('funenc_xa_station.break_type_increase_form').id
        return {
            'name': '故障类型',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_staion.break_type_increase',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def delete_record(self):

        self.unlink()
