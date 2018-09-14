# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields


class AwardRecord(models.Model):
    _name = 'funenc_xa_station.award_record'


    line_road = fields.Char(string='线路')
    station_site = fields.Char(string='站点')
    jobnumber = fields.Char(string='工号')
    staff = fields.Char(string='员工')
    position = fields.Char(string='职位')
    award_money = fields.Char(string='奖励金额')
    award_target_kind = fields.Char(string='奖励指标类')
    award_project = fields.Char(string='奖励项目')
    check_project = fields.Char(string='考核项目')
    incident_describe = fields.Char(string='事件描述')
    check_person = fields.Char(string='考评人')
    check_tiem = fields.Datetime(string='考评时间')

    @api.model
    def award_record_create(self):
        return {
            'type':'ir.actions.act_window',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'funenc_xa_station.award_record',
            # 'res_id':'',
            'context':self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }