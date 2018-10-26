# -*- coding: utf-8 -*-

import odoo.exceptions as msg
from odoo import models, fields, api

import datetime, time
from ..get_domain import get_domain

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
            this.leave_length = round( (time.mktime(end_work_time.timetuple()) - time.mktime(start_work_time.timetuple())+(24*60*60)) / (60 * 60), 2)

    @api.model
    @get_domain
    def get_day_plan_publish_action(self, domain):
        view_tree = self.env.ref('funenc_xa_station.funenc_xa_station_leave_list').id
        return {
            'name': '请假记录',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain': domain,
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.leave',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                           [
                               {'title': '考勤汇总(缺失)',
                               'action':  'funenc_xa_station.good_deeds_act',
                                'group':'funenc_xa_station.table_attendance_total',
                               },
                               {
                                   'title': '请假记录',
                                   'action2' : 'funenc_xa_station.xa_station_leave_list_action',
                                   'group' : 'funenc_xa_station.table_leave_record',
                               },
                               {
                                   'title': '打卡记录',
                                   'action2':  'funenc_xa_station.xa_station_clock_list_action',
                                   'group' : 'funenc_xa_station.table_card_record',
                               },
                              {
                                   'title': '加班记录',
                                   'action2':  'funenc_xa_station.xa_station_overtime_list_action',
                                   'group' : 'funenc_xa_station.table_overtime_record',
                               },
                           ]
                       }''',
            'context': self.env.context,
        }

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


    @api.model
    def get_leave_list(self):

        pass
