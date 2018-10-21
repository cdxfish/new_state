# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields


class TransceiverSettings(models.Model):
    _name = 'funenc_xa_station.transceiver_settings'
    _inherit = 'fuenc_station.station_base'

    transient_type = fields.Char(string='工器具类型')
    transient_name = fields.Char(string='工器具名称')
    transient_number = fields.Char(string='工器具编号')
    post = fields.Char(string='位置')
    state = fields.Selection([('one','正常'),('zero','故障')],string='状态')
    break_descrip = fields.Text(string='故障描述')
    # break_image = fields.One2many(string='故障图片')