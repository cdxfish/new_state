# -*- coding: utf-8 -*-
from odoo import models, fields, api
import odoo.exceptions as msg

class station_detail(models.Model):
    _name = 'funenc_xa_station.station_detail'
    _description = u'车站详情'


    station_nature = fields.Text(string='车站性质')
    station_position = fields.Text(string='车站位置')
    station_exit_information = fields.Text(string='出口信息')

    @api.model
    def create_station_detail(self):
        return {
            'name': '钥匙创建',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc.xa.station.key.detail',
            'context': self.env.context,
            # 'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

