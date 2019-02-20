# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CivilEngineering(models.Model):
    _name = 'funenc_xa_station.station_exit'
    _description = u'安全出口图'

    position= fields.Char(string='位置')
    exit_map = fields.Many2many('ir.attachment','station_exit_ir_attachment_1_ref','station_exit_id','ir_attachment_id',string='消防逃生图')

    station_master_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users',string='站长')
    station_mobile = fields.Char(related='station_master_id.mobile', string='电话')
    station_summary_id = fields.Many2one('funenc_xa_station.station_summary_id',string='车站详情')



    def station_exit_see(self):
        context = dict(self.env.context or {})
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_station_exit_see_form').id
        return {
            'name': '图片查看',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.station_exit',
            'context': context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
            "views": [[view_form, "form"]],
        }





