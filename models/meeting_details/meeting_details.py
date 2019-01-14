# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import datetime
from ..get_domain import get_domain

class MeetingDateils(models.Model):
    _name = 'funenc_xa_station.meeting_dateils'
    _inherit = ['fuenc_station.station_base','mail.thread','mail.activity.mixin']

    meeting_theme = fields.Char(string='会议主题', track_visibility='onchange')
    meeting_time = fields.Datetime(string='会议时间', track_visibility='onchange')
    # start_meet = fields.Datetime(string='会议开始时间',required=True)
    compere = fields.Char(string='主持人',required=True, track_visibility='onchange')
    join_person = fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_users','meet_detaails_rel',string='参会人员', track_visibility='onchange')
    meeting_content = fields.Text(string='会议内容',required=True, track_visibility='onchange')
    meeting_site = fields.Char(string='会议地点',required=True, track_visibility='onchange')
    recorder = fields.Char(string='记录人',default=lambda self: self.default_person_id(), track_visibility='onchange')
    record_time = fields.Char(string='记录日期',default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), track_visibility='onchange')
    load_file_test = fields.Many2many('ir.attachment','funenc_xa_station_meeting_dateils_ir_attachment_rel',
                                         'attachment_id','meeting_dateils_id', string='图片上传', track_visibility='onchange')
    files_accessory = fields.Many2many('ir.attachment','funenc_xa_station_file_ir_attachment_rel',
                                      'station_id','file_id', string='文件附件', track_visibility='onchange')
    shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班', track_visibility='onchange')

    # 创建一条新的记录
    @get_domain
    def new_increase_record(self,domain):
        view_form = self.env.ref('funenc_xa_station.meeting_details_form').id
        return {
            'name': '会议记录',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'domain':domain,
            'res_model': 'funenc_xa_station.meeting_dateils',
            'target': 'new',
        }

    # 自动获取记录人的姓名
    @api.model
    def default_person_id(self):
        if self.env.user.id ==1:
            return

        return self.env.user.dingtalk_user.name

    def meet_dateils_button(self):
        view_form = self.env.ref('funenc_xa_station.meeting_details_details').id
        return {
            'name': '证件名称',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
            'res_model': 'funenc_xa_station.meeting_dateils',
            'res_id': self.id,
            'flags': {'initial_mode': 'readonly'},
            # 'target': 'new',
        }

    def meet_change_button(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.meeting_dateils',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'target': 'new',
        }
    def meet_delete_button(self):
        self.env['funenc_xa_station.meeting_dateils'].search([('id','=',self.id)]).unlink()

    # @api.constrains('start_meet','end_meet')
    # def date_change(self):
    #     for i in self:
    #         if str(i.start_meet)[:10] == str(i.end_meet)[:10]:
    #             i.meeting_time = str(i.start_meet) + ' ——' + str(i.end_meet)[10:]
    #         else:
    #             i.meeting_time = str(i.start_meet) + ' ——' + str(i.end_meet)

    @api.model
    @get_domain
    def get_day_plan_publish_action(self,domain):
        view_tree = self.env.ref('funenc_xa_station.meeting_details_tree').id
        return {
            'name': '会议记录',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain':domain,
            "views": [[view_tree, "tree"]],
            'res_model': 'funenc_xa_station.meeting_dateils',
            'context': self.env.context,
        }






