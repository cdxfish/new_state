# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import datetime

class MeetingDateils(models.Model):
    _name = 'funenc_xa_station.meeting_dateils'
    _inherit = 'fuenc_station.station_base'

    meeting_theme = fields.Char(string='会议主题',required=True)
    meeting_time = fields.Char(string='会议时间',computed='date_change',store=True)
    start_meet = fields.Datetime(string='会议开始时间',required=True)
    end_meet = fields.Datetime(string='会议结束时间',required=True)
    compere = fields.Char(string='主持人',required=True)
    join_person = fields.Many2many('cdtct_dingtalk.cdtct_dingtalk_users','meet_detaails_rel',string='参会人员')
    meeting_content = fields.Text(string='会议内容',required=True)
    meeting_site = fields.Char(string='会议地点',required=True)
    recorder = fields.Char(string='记录人',default=lambda self: self.default_person_id())
    record_time = fields.Char(string='记录日期',default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    load_file_test = fields.Many2many('ir.attachment','funenc_xa_station_meeting_dateils_ir_attachment_rel',
                                         'attachment_id','meeting_dateils_id', string='图片上传')
    files_accessory = fields.One2many('ir.attachment','res_id', string='文件附件')
    shifts_id = fields.Many2one('funenc_xa_station.production_change_shifts', string='交接班')

    # 创建一条新的记录
    def new_increase_record(self):
        view_form = self.env.ref('funenc_xa_station.meeting_details_form').id
        return {
            'name': '会议记录',
            'type': 'ir.actions.act_window',
            "views": [[view_form, "form"]],
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

    @api.constrains('start_meet','end_meet')
    def date_change(self):
        for i in self:
            if str(i.start_meet)[:10] == str(i.end_meet)[:10]:
                i.meeting_time = str(i.start_meet) + ' ——' + str(i.end_meet)[10:]
            else:
                i.meeting_time = str(i.start_meet) + ' ——' + str(i.end_meet)






