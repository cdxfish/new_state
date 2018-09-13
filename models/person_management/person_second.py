# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api,models,fields
import time
import datetime
class PersonSecond(models.Model):
    _name = 'person_management.person_second'

    person_number = fields.Char(related='user_id.jobnumber',string="工号")
    user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='')
    line_road = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='线路')
    station = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='车站')
    per_site = fields.Text(related='user_id.position',string='岗位')
    second_line = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='借调线路')
    second_station = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department',string='借调车站')
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
                        this.second_line = False
                        this.second_station = False
            else:
                this.operat_time = 'zero'

    @api.onchange('line_road')
    def change_line_road(self):
        # 这是通用应该默认本线路，本部门

        if not self.line_road:
            return

        department_id = self.line_road.departmentId
        child_department_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([('parentid', '=', department_id)]).ids

        return {'domain':{'station':[('id','in', child_department_ids)]},
                'value':{'station': None}
                }

    @api.onchange('station')
    def change_user(self):
        if not self.station:
                return {'value': {'user_id': None}
                }

        department_id = self.station.id
        # user_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([('users', '=', department_id)]).ids
        sql ='select user_id from cdtct_dingtalk_user_department_rel where department_id = {}'.format(department_id)
        self.env.cr.execute(sql)
        user_ids = [user.get('user_id') for user in  self.env.cr.dictfetchall()]
        return {'domain': {'user_id': [('id','in', user_ids)]},
                'value': {'user_id': None}
                }

class DepartmentInherit(models.Model):
    _inherit = 'cdtct_dingtalk.cdtct_dingtalk_department'

    person_second_id = fields.One2many('person_management.person_second','second_station',string='')
