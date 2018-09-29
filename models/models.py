# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.exceptions as msg


class fuenc_station(models.Model):
    _name = 'fuenc_station.station_base'

    site_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='站点', default=lambda self: self.default_site_id())
    line_id = fields.Many2one('cdtct_dingtalk.cdtct_dingtalk_department', string='线路', default=lambda self: self.default_line_id())


    @api.model
    def default_line_id(self):
        if self.env.user.id ==1:
            return

        return self.env.user.dingtalk_user.line_id.id

    @api.model
    def default_site_id(self):
        if self.env.user.id ==1:
            return

        return self.env.user.dingtalk_user.departments[0].id

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
                model = self._table

                site_id = self.env.user.dingtalk_user.departments[0].id
                line_id = self.env.user.dingtalk_user.line_id.id
                #   不用orm  因为会递归回调
                sql = 'update {} set site_id = {}, line_id = {} where id = {}'.format(model,site_id,line_id,self.id)
                self.env.cr.execute(sql)


    @api.onchange('line_id')
    def change_line_id(self):
        if not self.line_id:
            return

        department_id = self.line_id.departmentId
        child_department_ids = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
            [('parentid', '=', department_id)]).ids

        return {'domain': {'site_id': [('id', 'in', child_department_ids)]}
                # 'value': {'site_id': None}
                }
