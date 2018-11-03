# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SignalSystem(models.Model):
    _name = 'funenc_xa_station2.signal_system'
    _description = u'信号系统'
    _inherit = 'fuenc_station.station_base'

    name= fields.Char(string='', default=' ')
    signal_machine_ids = fields.One2many('funenc_xa_station2.signal_machine', 'signal_system_id', string='信号机位置编号')


class SignalMachine(models.Model):
    _name = 'funenc_xa_station2.signal_machine'
    _description = u'信号机'
    _rec_name = ''

    signal_machine_no = fields.Char(string='编号')
    position_distance = fields.Char(string='位置里程')
    purpose = fields.Char(string='用途')
    type = fields.Char(string='类型')
    excursus = fields.Char(string='附记')

    signal_system_id = fields.Many2one('funenc_xa_station2.signal_system')