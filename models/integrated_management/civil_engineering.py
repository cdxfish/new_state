# -*- coding: utf-8 -*-
from odoo import models, fields, api
from ..get_domain import get_domain

class CivilEngineering(models.Model):
    _name = 'funenc_xa_station.civil_engineering'
    _description = u'土建结构'
    _inherit = 'fuenc_station.station_base'



class EssentialInformation(models.Model):
    _name = 'funenc_xa_station.essential_information'
    _description = u'基本信息'
    _rec_name = 'type'

    type = fields.Char(string= '类别')
    content = fields.Text(string= '内容')

    civil_engineering_id = fields.Many2one('funenc_xa_station.station_summary',string='出口信息')


class PrivateChannel(models.Model):
    _name = 'funenc_xa_station.private_channel'
    _description = u'专用通道信息'
    _rec_name = 'name'

    name = fields.Char(string='通道名称')
    channel_width = fields.Char(string='宽度(m)')
    remarks = fields.Text(string='说明')

    civil_engineering_id = fields.Many2one('funenc_xa_station.station_summary', string='出口信息')

