# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.exceptions as msg


class fuenc_station(models.Model):
    _name = 'fuenc_station.station_base'

    site_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='站点')
    line_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='线路')

    @api.constrains('site_id', 'line_id')
    def compute_site_and_line(self):
        if self.env.user.id == 1:
            if not self.line_id:
                raise msg.Warning('线路不能为空')

            if not self.site_id:
                raise msg.Warning('车站不能为空')
        else:
            ding_user = self.env.user.dingtalk_user[0]
            department = ding_user.departments[0]
            if department.department_hierarchy == 3:
                self.site_id = self.env.user.user[0].site_id
                self.site_id = self.env.user.user[0].line_id
