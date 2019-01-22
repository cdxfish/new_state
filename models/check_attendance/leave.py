# -*- coding: utf-8 -*-

import odoo.exceptions as msg
from odoo import models, fields, api

import datetime, time
from ..get_domain import get_domain


class Leave(models.Model):
    _name = 'funenc_xa_station.leave'
    _description = '请假记录'
    _inherit = ['fuenc_station.station_base', 'mail.thread', 'mail.activity.mixin']
    _order = 'leave_start_time desc'
    _rec_name = 'leave_user_id'

    KEY = [('sick_leave', '病假'),
           ('maternity_leave', '孕假'),
           ('compassionate_leave', '事假'),
           ('annual_leave', '年假'),
           ('marital_leave', '婚假'),
           ('maternity_eave_1', '产假'),
           ('nursing', '护理'),
           ('funeral_leave', '丧假'),
           ('injury_leave', '工伤假'),
           ('leave_office', '离职')
           ]

    leave_user_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='请假人员', required=True, track_visibility='onchange')
    jobnumber = fields.Char(related='leave_user_id.jobnumber', string="工号", track_visibility='onchange')
    position = fields.Text(related='leave_user_id.position', string="职位", track_visibility='onchange')
    leave_type = fields.Selection(selection=KEY, string='请假类型', required=True, track_visibility='onchange')
    leave_start_time = fields.Datetime(string='请假开始时间', required=True, track_visibility='onchange')
    leave_end_time = fields.Datetime(string='请假结束时间', required=True, track_visibility='onchange')
    leave_length = fields.Float(string='请假时长(h)', digits=(10000000, 2), compute='_compute_leave_length')
    leave_reason = fields.Text(string='请假原因', track_visibility='onchange')
    application_time = fields.Datetime(string='申请时间', track_visibility='onchange')
    approve_user = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_users', string='审批人', track_visibility='onchange')

    def _compute_leave_length(self):
        for this in self:
            start_work_time = datetime.datetime.strptime(this.leave_start_time, '%Y-%m-%d %H:%M:%S')
            end_work_time = datetime.datetime.strptime(this.leave_end_time, '%Y-%m-%d %H:%M:%S')
            this.leave_length = round(
                (time.mktime(end_work_time.timetuple()) - time.mktime(start_work_time.timetuple()) + (24 * 60 * 60)) / (
                        60 * 60), 2)

    @api.model
    @get_domain
    def get_day_plan_publish_action(self, domain):
        view_tree = self.env.ref('funenc_xa_station.funenc_xa_station_leave_list').id
        if self.env.user.id ==1:
            domain_id = []
        else:
            domain_id = [['leave_user_id','=',self.env.user.dingtalk_user.id]]
        return {
            'name': '请假记录',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain': domain_id,
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.leave',
            "top_widget": "multi_action_tab",
            "top_widget_key": "driver_manage_tab",
            "top_widget_options": '''{'tabs':
                            [
                                {'title': '打卡记录',
                                'action':  'funenc_xa_station.xa_station_clock_list_action',
                                'group':'funenc_xa_station.table_card_record',
                                },
                                {
                                    'title': '加班记录',
                                    'action2' : 'funenc_xa_station.xa_station_overtime_list_action',
                                    'group' : 'funenc_xa_station.table_overtime_record',
                                    },
                                {
                                    'title': '请假记录',
                                    'action2':  'funenc_xa_station.xa_station_leave_list_action',
                                    'group' : 'funenc_xa_station.table_leave_record',
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

    @api.model
    def save(self):
        leave_user_id = self.leave_user_id  # 请假人
        site_id = leave_user_id.departments[0].id
        vacation_id = self.env['funenc_xa_station.sheduling_record'].search(
            [('site_id', '=', site_id), ('is_vacation', '=', 1)]).id  # 休假
        leave_start_time = self.leave_start_time  # 请假开始时间
        leave_end_time = self.leave_end_time  # 请假结束时间
        sheduling_records = self.env['funenc_xa_station.sheduling_record'].search(
            [('sheduling_date', '>=', leave_start_time), ('sheduling_date', '<=', leave_end_time)])
        for sheduling_record in sheduling_records:
            # if sheduling_record.arrange_order_id.is_vacation == 1:
            sheduling_record.arrange_order_id = vacation_id

        # 考勤   更改  必须出排班 不然排班改不了
        start_datetime = datetime.datetime.strptime(leave_end_time, '%Y-%m-%d')
        days = (start_datetime - datetime.datetime.strptime(leave_start_time, '%Y-%m-%d')).days + 1
        # clock_records = self.env['fuenc_station.clock_record'].search(
        #     [('time', '>=', leave_start_time), ('time', '<=', leave_end_time), ('user_id', '=', leave_user_id)])
        time_days = []

        for day in range(days):
            str_to_datetime = start_datetime + datetime.timedelta(days=day)
            time_days.append(str_to_datetime)

        for time_day in time_days:
            self.env['fuenc_station.clock_record'].create({
                'arrange_order_id': vacation_id,
                'is_leave': 1,
                'show_value': self.leave_type,
                'time': time_day,
                'user_id': leave_user_id
            })

    def create_record(self):
        view_form = self.env.ref('funenc_xa_station.funenc_xa_station_leave_form').id
        return {
            'name': '新建请假',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.leave',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    def save_record(self):
        pass
