# !user/bin/env python3
# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ConsumablesSummary(models.Model):

    _name = 'funenc_xa_station.consumables_summary'

    @api.model
    def init_methods_action(self):
        lis= []
        record = self.env['funenc_xa_station.consumables_type'].search([])
        for i in record:
            count_one = 0
            dic = {}
            dic['consumables_type'] = i.consumables_type
            count = self.env['funenc_xa_station.consumables_inventory'].search([("consumables_type", "=", i.id)])
            for count_self in count:
                count_one += count_self.inventory_count
            dic['inventory'] = count_one
            lis.append(dic)
        return lis


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

    @api.model
    def search_record_consumables(self,**kw):
        lis= []
        if kw.get('department'):
            dic_department_id = {1: kw.get('department')}  #部门
        if kw.get('line'):
            dic_line_id = {2: kw.get('line') } # 线路
        if kw.get('site'):
            dic_line_id = {3: kw.get('line')} # 站点

        

        record = self.env['funenc_xa_station.consumables_inventory'].search([('consumables_type','=',2)])
        return lis


