# !user/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api,models,fields
import requests
import urllib
import base64

class VideoVoice(models.Model):
    _name = 'video_voice_model'

    video = fields.Binary(string='上传附件')
    file_name = fields.Char(string='File Name')
    url = fields.Char(string='url')
    mp_play_one = fields.Many2one(string='视频附件的附件')

    @api.model
    def create(self, params):
        video_attachment = self.env['fuenc_xa_station.guests_hurt'].search([])
        file_binary = params['video']
        file_name = params.get('file_name', self.file_name)
        if file_binary:
            url = self.env['qiniu_service.qiniu_upload_bucket'].upload_data(
                'funenc_xa_station', file_name, base64.b64decode(file_binary))
            params['url'] = url
            params['file_name'] = file_name
        return super(VideoVoice, self).create(params)

    def view_details(self):
        url = self.url
        if url:
            return {
                "type": "ir.actions.act_url",
                "url": url,
                "target": "new"
            }