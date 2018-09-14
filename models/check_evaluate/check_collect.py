# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields


class CheckCollect(models.Model):
    _name = 'funenc_xa_station.check_collect'

    line_road = fields.Char(string='线路')
    station_site = fields.Char(string='站点')
    jobnumber = fields.Char(string='工号')
    staff = fields.Char(string='员工')
    position = fields.Char(string='职位')
    all_score = fields.Integer(string='总分值')
    mouth_grade = fields.Integer(string='本月评分')
    grade_degree = fields.Integer(string='考评次数')
