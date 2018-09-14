# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields


class AwardCollect(models.Model):
    _name = 'funenc_xa_station.award_collect'

    line_road = fields.Char(string='线路')
    station_site = fields.Char(string='站点')
    jobnumber = fields.Char(string='工号')
    staff = fields.Char(string='员工')
    position = fields.Char(string='职位')
    award_money = fields.Integer(string='奖励金额')
    award_degree = fields.Integer(string='奖励次数')