# -*- coding: utf-8 -*-
from odoo import models, fields, api
import odoo.exceptions as msg

class station_detail(models.Model):
    _name = 'funenc_xa_station.station_detail'
    _description = u'车站详情'

    name = fields.Char(string='车站名字')
    station_nature = fields.Text(string='车站性质')
    station_position = fields.Text(string='车站位置')
    current_location = fields.Char(string='当前位置')
    station_exit_information = fields.One2many('funenc_xa_station.station_exit_information','station_id', string='出口信息')
    station_map_images = fields.One2many('funenc_xa_station.station_map_images', 'station_detail_id', string='地面信息图',required= True)


    @api.model
    def create_station_detail(self):
        return {
        }


class StationExitInformation(models.Model):
    _name = 'funenc_xa_station.station_exit_information'
    _description = u'出口信息'
    _rec_name = 'position'

    exit_no = fields.Char(string='出口编号')
    exit_width = fields.Char(string='宽度')
    position = fields.Char(string='位置')
    remarks = fields.Text(string='备注说明')
    station_id = fields.Many2one('funenc_xa_station.station_detail',string='车站')


class StationMapImages(models.Model):
    _name = 'funenc_xa_station.station_map_images'
    _description = u'地面信息'

    name = fields.Char(string='名称')
    image = fields.Binary(string='图片')
    station_detail_id = fields.Many2one('funenc_xa_station.station_detail',string='车站详情相关')


