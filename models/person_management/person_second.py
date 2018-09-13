# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api,models,fields
import time
import datetime
class PersonSecond(models.Model):
    _name = 'person_management.person_second'

    person_number = fields.Char(string="工号")
    name = fields.Char(string='姓名')
    line_road = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='线路')
    station = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='车站')
    per_site = fields.Char(string='岗位')
    second_line = fields.Char(string='借调线路')
    second_station = fields.Char(string='借调车站')
    second_time = fields.Date(string='借调开始时间')
    second_end_time = fields.Date(string='借调结束时间')
    operator = fields.Char(string='操作人')
    operat_time = fields.Selection([('one','正常'),(('zero','已过期'))],string='状态',compute='compute_time_status',readonly=True)

    def second_delect(self):
        self.env['person_management.person_second'].search([('id', '=', self.id)]).unlink()

    def second_modification(self):
        return {
            'name': '人员借调',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'person_management.person_second',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def person_details(self):
        pass


    def compute_time_status(self):
        for this in self:
            if this.second_end_time:
                local_time = time.time()
                time1 = this.second_end_time

                time01 = datetime.datetime.strptime(time1,'%Y-%m-%d')+datetime.timedelta(days=+1)
                time2 = time.mktime(time01.timetuple())
                if local_time - time2 <= 0:
                    if this.operat_time != 'one':
                        this.operat_time = 'one'
                else:
                    if this.operat_time != 'zero':
                        this.operat_time = 'zero'
            else:
                this.operat_time = 'zero'
