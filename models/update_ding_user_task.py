# -*- coding: utf-8 -*-
from odoo import models, api


class update_ding_user_task(models.Model):
    _name = 'funenc_xa_station.update_ding_user_task'
    _description = u'同步人钉钉任务'

    @api.model
    def update_ding_user_task(self):
        self.env['cdtct_dingtalk.cdtct_dingtalk_account'].search([])[0].sync_dingtalk()
