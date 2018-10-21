# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields


class TransientBreakManagement(models.Model):
    _name = 'funenc_xa_station.transient_break_management'
    _inherit = 'fuenc_station.station_base'

    transceiver_type = fields.Char(string='工器具类型')
    transceive_name = fields.Char(string='工器具名称')
    transceive_number = fields.Char(string='工器具编号')
    post = fields.Char(string='位置')
    apply_name = fields.Char(string='申报时间')
    break_describe = fields.Char(string='故障描述')
    break_image = fields.Binary(string='故障图片')
    state = fields.Selection([('one','正常'),('zero','故障')],string='状态')
    repair_imange = fields.Datetime(string='修复时间')
    repair_manufacturer = fields.Char(string='修复厂家')
    after_repair_image = fields.Binary(string='修复后的图片')




