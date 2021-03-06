# -*- coding: utf-8 -*-
from odoo import models, fields, api



class LineMap(models.Model):
    _name = 'funenc_xa_station.line_map'
    _description = u'车站线路平面图'
    _rec_name = 'name'

    name = fields.Char(string='名称')
    image = fields.Binary(string='图片')

    line_turnout_id = fields.Many2one('funenc_xa_station.station_summary',string='线路道岔')


class Turnout(models.Model):
    _name = 'funenc_xa_station.turnout'
    _description = u'道岔'
    _rec_name = 'turnout_no'

    turnout_no = fields.Char(string='道岔编号')
    turnout_no_1 = fields.Char(string='道岔辙岔号')
    chain_mode = fields.Char(string='联锁方式')
    key_Safekeeping = fields.Char(string='钥匙保管地点')
    operation_staff = fields.Char(string='操纵人员')
    allow_speed = fields.Char(string='侧向允许通过速度km/h')
    position_distance = fields.Char(string='位置里程')


    line_turnout_id = fields.Many2one('funenc_xa_station.station_summary', string='线路道岔')

class LiaisonStation(models.Model):
    _name = 'funenc_xa_station.liaison_station'
    _description = u'联络站基本信息'
    _rec_name = 'service_channel'

    service_channel = fields.Char(string='联络通道')
    position_distance = fields.Char(string='位置/里程')
    interval = fields.Char(string='区间')
    remarks = fields.Char(string='备注')

    line_turnout_id = fields.Many2one('funenc_xa_station.station_summary', string='线路道岔')

class OperatingLine(models.Model):
    _name = 'funenc_xa_station.operating_line'
    _description = u'联络站基本信息'
    _rec_name = 'position'

    position = fields.Char(string='位置')
    equipment = fields.Char(string='设备')
    departure_point = fields.Char(string='设计起点里程')
    destination = fields.Char(string='终点')
    length = fields.Char(string='长度')
    line_id = fields.Char(string='线别')
    purpose = fields.Char(string='用途')


    line_turnout_id = fields.Many2one('funenc_xa_station.station_summary', string='线路道岔')