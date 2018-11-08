# -*- coding: utf-8 -*-

from odoo import api, models, fields


class StationSummary(models.Model):
    _name = 'funenc_xa_station.station_summary'

    civil_engineering = fields.One2many('funenc_xa_station.civil_engineering','contact_re',string='土建结构关联表')
    station_detail = fields.One2many('funenc_xa_station.station_detail','contact_re',string='车站详情关联表')
    ground_traffic = fields.One2many('funenc_xa_station.ground_traffic','contact_re',string='地面交通关联表')