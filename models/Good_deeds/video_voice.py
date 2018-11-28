# !user/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api,models,fields
import requests
import urllib
import base64

class VideoVoice(models.Model):
    _name = 'video_voice_model'

    def _default_associated(self):
        if self._context.get('active_id', False):
            return self._context['active_id']

    video = fields.Binary(string='文件')
    file_name = fields.Char(string='File Name')
    url = fields.Char(string='url')
    guests_mp_play_one = fields.Many2one('fuenc_xa_station.guests_hurt',string='客人受伤视频附件的附件')
    guests_mp3_play = fields.Many2one('fuenc_xa_station.guests_hurt',string='客人受伤的录音附件')
    add_guest_play_mp4 = fields.Many2one('fuenc_station.good_deeds',string='增加好人好事附件')
    add_guest_play_mp3 = fields.Many2one('fuenc_station.good_deeds',string='增加好人好事录音附件')
    good_deeds_play = fields.Many2one('fuenc_station.good_deeds',string='好人好事录音附件')
    suggest_box_video = fields.Many2one('funenc_xa_station.suggestion_box',string='乘客意见箱视屏附件')
    suggest_box_audio = fields.Many2one('funenc_xa_station.suggestion_box',string='乘客意见箱音频附件')
    site_drill_plan_audio = fields.Many2one('funenc_xa_station.site_drill_plan',string='站点演练详情视屏附件')
    special_money_act = fields.Many2one('funenc_xa_station.special_money',string='特殊赔偿金处理结果附件',default=_default_associated)
    belong_management_imange = fields.Many2one('funenc_xa_station.belong_to_management',string='属地管理')

    @api.model
    def create(self, params):
        video_attachment = self.env['fuenc_xa_station.guests_hurt'].search([])
        if params.get('video'):
            file_binary = params['video']
            file_name = params.get('file_name', self.file_name)
            if file_binary:
                url = self.env['qiniu_service.qiniu_upload_bucket'].upload_data(
                    'funenc_xa_station', file_name, base64.b64decode(file_binary))
                params['url'] = url
                params['file_name'] = file_name
            return super(VideoVoice, self).create(params)
        return super(VideoVoice, self).create(params)

    def view_details(self):
        url = self.url
        if url:
            return {
                "type": "ir.actions.act_url",
                "url": url,
                "target": "new"
            }

    def image_button_act(self):
        load_file_form = self.env.ref('funenc_xa_station.video_voice_load').id
        return {
            'name': '文件',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[load_file_form, "form"]],
            'res_model': 'video_voice_model',
            'context': self.env.context,
            'flags': {'initial_mode': 'readonly'},
            'res_id': self.id,
            'target': 'new',
        }


    def load_file(self):
        load_file_form = self.env.ref('funenc_xa_station.video_voice_load').id
        return {
            'name': '文件',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            "views": [[load_file_form, "form"]],
            'res_model': 'video_voice_model',
            'context': self.env.context,
            'flags': {'initial_mode': 'readonly'},
            'res_id': self.id,
            'target': 'new',
        }