# -*- coding: utf-8 -*-

import odoo.exceptions as msg
from odoo import models, fields, api

import datetime, time


class Leave(models.Model):
    _name = 'funenc_xa_station.leave'
    _description = '请假模型'
    _inherit = 'fuenc_station.station_base'

    KEY = [('sick_leave', '病假'),
           ('maternity_leave', '孕假'),
           ('compassionate_leave', '病假'),
           ('annual_leave', '年假'),
           ('marital_leave', '婚假'),
           ('maternity_eave_1', '产假'),
           ('nursing', '护理'),
           ('funeral_leave', '丧假'),
           ('injury_leave', '工伤假'),
           ('leave_office', '离职')
           ]

    leave_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='请假人员', required=True)
    jobnumber = fields.Char(related='leave_user_id.jobnumber', string="工号")
    position = fields.Text(related='leave_user_id.position', string="职位")
    leave_type = fields.Selection(selection=KEY, string='请假类型', required=True)
    leave_start_time = fields.Datetime(string='请假开始时间', required=True)
    leave_end_time = fields.Datetime(string='请假结束时间', required=True)
    leave_length = fields.Float(string='请假时长(h)', digits=(10000000, 2), compute='_compute_leave_length')
    leave_reason = fields.Text(string='请假原因')
    application_time = fields.Datetime(string='申请时间')
    approve_user = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='审批人')

    def _compute_leave_length(self):
        for this in self:
            start_work_time = datetime.datetime.strptime(this.leave_start_time, '%Y-%m-%d %H:%M:%S')
            end_work_time = datetime.datetime.strptime(this.leave_end_time, '%Y-%m-%d %H:%M:%S')
            this.leave_length = round(
                (time.mktime(end_work_time.timetuple()) - time.mktime(start_work_time.timetuple())) / (60 * 60), 2)

    @api.model
    def create_leave(self):
        return {
            'name': '新增请假',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.leave',
            'context': self.env.context,
            'target': 'new',
        }

    def edit(self):
        return {
            'name': '请假详情编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.leave',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }

    def delete(self):
        self.unlink()