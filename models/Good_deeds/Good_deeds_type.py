# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api,models,fields


class GoodDeedsType(models.Model):
    _name = 'funenc_xa_station.good_deeds_type'
    _rec_name = 'good_type'

    good_type = fields.Char(string='好人好事类型')
    note = fields.Char(string='备注')

    def onchange_typr_action(self):

        return {
            'name': '特殊赔偿金详情',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.good_deeds_type',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def good_delete_action(self):
        self.env['funenc_xa_station.good_deeds_type'].search([('id','=',self.id)]).unlink()