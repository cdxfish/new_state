# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StationExitInformation(models.Model):
    _name = 'funenc_xa_station.station_exit_information'
    _description = u'出口信息'
    _rec_name = 'position'

    exit_no = fields.Char(string='出口编号')
    exit_width = fields.Char(string='宽度')
    position = fields.Char(string='位置')
    remarks = fields.Text(string='备注说明')
    station_id = fields.Many2one('funenc_xa_station.station_summary',string='车站')


class StationMapImages(models.Model):
    _name = 'funenc_xa_station.station_map_images'
    _description = u'地面信息'

    name = fields.Char(string='名称')
    image = fields.Binary(string='图片')
    station_detail_id = fields.Many2one('funenc_xa_station.station_summary',string='车站详情相关')


