# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api,models,fields

class PersonSecond(models.Model):
    _name = 'person_management.person_second'

    person_number = fields.Char(string="工号")
    name = fields.Char(string='姓名')
    line_road = fields.Char(string='线路')
    station = fields.Char(string='车站')
    per_site = fields.Char(string='岗位')
    second_line = fields.Char(string='借调线路')
    second_station = fields.Char(string='借调车站')
    second_time = fields.Char(string='借调时间')
    operator = fields.Char(string='操作人')
    operat_time = fields.Selection([('one','正常'),(('zero','已过期'))],string='状态')

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