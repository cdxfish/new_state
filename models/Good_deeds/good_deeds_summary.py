# !user/bin/env python3
# -*- coding: utf-8 -*-
from odoo import api, fields, models


class GoodDeedsSummary(models.Model):
    _name = 'funenc_xa_station.good_deeds_summary'

    @api.model
    def init_methods_action(self):
        lis = []
        type =  self.env['funenc_xa_station.good_deeds_type'].search_read([],['good_type'])
        for i in type:
            dic = {}
            count = self.env['fuenc_station.good_deeds'].search([('type','=',i.get('id'))])
            dic['good_deeds_type'] = i.get('good_type')
            dic['frequency'] = len(count)
            lis.append(dic)
        return lis

    @api.model
    def get_department(self):
        lis = []

        department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([('department_hierarchy','=',1)])
        for i in department:
            dic = {}
            dic['name']=i.name
            dic['id']=i.id
            lis.append(dic)
        return lis

    @api.model
    def get_line(self,date):
        lis = []
        department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id','=',date)],['departmentId'])
        name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([('parentid','=',department[0].get('departmentId'))])
        for i in name:
            dic = {}
            dic['name']=i.name
            dic['id']=i.id
            lis.append(dic)
        return lis

    @api.model
    def get_site(self,date):
        lis = []
        department = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id','=',date)],['departmentId'])
        name = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search([('parentid','=',department[0].get('departmentId'))])
        for i in name:
            dic = {}
            dic['name']=i.name
            dic['id']=i.id
            lis.append(dic)
        return lis






