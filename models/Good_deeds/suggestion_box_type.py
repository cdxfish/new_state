# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api,models,fields


class SuggestBoxTy(models.Model):
    _name = 'funenc_xa_station.suggest_box_type'

    suggest_box = fields.Char(string='意见信箱类型')
    note = fields.Char(string='备注')

    def onchange_typr_action(self):
        return {
            'name': '证件名称',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.suggest_box_type',
            'context': self.env.context,
            'res_id':self.id,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def good_delete_action(self):
        self.env['funenc_xa_station.suggest_box_type'].search([('id','=',self.id)]).unlink()
