# -*- coding: utf-8 -*-
from odoo import models, fields, api

class StationStaffing(models.Model):
    _name = 'funenc_xa_station.station_staffing'
    _description = u'信号系统'

    staff_no = fields.Char(string='工号')
    staff_name = fields.Char(string='名字')
    staff_property = fields.Selection(selection=[('site','本站'), ('loan', '借调')],default= 'site', string='人员属性')
    staff_phone = fields.Char(string='电话')
    staff_position = fields.Char(string='职位')
    line_id = fields.Char(string='所属线路')
    site_id = fields.Char(string='所属车站')
    certificate_situation = fields.Char(string='证书情况')


