# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import api, models, fields


class MeetingDateils(models.Model):
    _name = 'funenc_xa_station.meeting_dateils'

    meeting_theme = fields.Char(string='会议主题')
    meeting_time = fields.Char(string='会议时间')
    compere = fields.Char(string='主持人')
    meeting_site = fields.Char(string='会议地点')
    recorder = fields.Char(string='记录人')
    record_time = fields.Datetime(string='记录时间')
    picture_accessory = fields.Char(string='图片附件')
    files_accessory = fields.Char(string='文件附件')



