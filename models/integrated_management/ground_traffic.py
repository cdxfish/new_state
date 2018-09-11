# -*- coding: utf-8 -*-
from odoo import models, fields, api

class GroundTraffic(models.Model):
    _name = 'funenc_xa_station.ground_traffic'
    _description = u'地面交通'
    _rec_name = 'ground_environment_ids'

    ground_environment_ids = fields.One2many('funenc_xa_station.ground_environment','ground_traffic_id',string='地面环境')
    bus_lines =  fields.One2many('funenc_xa_station.bus_line','ground_traffic_id',string='交通线路表')


class BusLine(models.Model):
    _name = 'funenc_xa_station.bus_line'
    _description = u'交通线路表'
    _rec_name = 'entrance_exit'

    entrance_exit = fields.Char(string='出入口')
    bus_station = fields.Char(string='公交站点')
    distance = fields.Char(string='距离')
    go_to = fields.Char(string='运行方向')
    bus_line = fields.Char(string='公交线路')

    ground_traffic_id = fields.Many2one('funenc_xa_station.ground_traffic',string='地面交通关联')


class GroundEnvironment(models.Model):
    _name = 'funenc_xa_station.ground_environment'
    _description = u'地面环境'
    _rec_name = 'entrance_exit'

    entrance_exit = fields.Char(string='出入口')
    one_grade_information = fields.Char(string='一级信息')
    two_grade_information = fields.Char(string='二级信息')
    three_grade_information = fields.Char(string='三级信息')
    ground_traffic_id = fields.Many2one('funenc_xa_station.ground_traffic',string='地面交通关联')

