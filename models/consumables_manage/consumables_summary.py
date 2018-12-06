# !user/bin/env python3
# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ConsumablesSummary(models.Model):
    _name = 'funenc_xa_station.consymbles_summary'

    @api.model
    def init_methods_action(self):
        return

    @api.model
    def get_department(self):
        lis = []

        department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([('department_hierarchy', '=', 1)])
        for i in department:
            dic = {}
            dic['name'] = i.name
            dic['id'] = i.id
            lis.append(dic)
        return lis

    @api.model
    def get_line(self, date):
        lis = []
        department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id', '=', date)],
                                                                                      ['departmentId'])
        name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
            [('parentid', '=', department[0].get('departmentId'))])
        for i in name:
            dic = {}
            dic['name'] = i.name
            dic['id'] = i.id
            lis.append(dic)
        return lis

    @api.model
    def get_site(self, date):
        lis = []
        department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id', '=', date)],
                                                                                      ['departmentId'])
        name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search(
            [('parentid', '=', department[0].get('departmentId'))])
        for i in name:
            dic = {}
            dic['name'] = i.name
            dic['id'] = i.id
            lis.append(dic)
        return lis
