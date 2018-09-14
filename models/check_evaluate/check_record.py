# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields

class CheckRecord(models.Model):
    _name = 'funenc_xa_station.check_record'

    line_road = fields.Char(string='线路')
    station_site = fields.Char(string='站点')
    job_number = fields.Integer(string='工号')
    position = fields.Char(string='职位')
    grade = fields.Char(string='评分')
    check_target = fields.Char(string='考评指标')
    problem_kind =fields.Char(string='问题类型')
    check_kind = fields.Char(string='考核项目')
    incident_describe = fields.Char(string='事件描述')
    check_person = fields.Char(string='考评人')
    check_time = fields.Datetime(string='考评时间')

    @api.model
    def new_add_record(self):
        return {
            'type':'ir.actions.act_window',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'funenc_xa_station.check_record',
            # 'res_id':'',
            'context':self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }